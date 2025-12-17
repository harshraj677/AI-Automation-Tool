<?php
/**
 * Smart Text Assistant - API Endpoint
 * 
 * This file handles all API requests from the frontend
 * Processes text using AI automation logic
 * 
 * @author Dinzin Developer Intern Candidate
 * @version 1.0.0
 */

// ========================================
// CONFIGURATION & INITIALIZATION
// ========================================
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Only allow POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode([
        'status' => 'error',
        'message' => 'Method not allowed. Only POST requests are accepted.'
    ]);
    exit();
}

// Include configuration file
require_once 'config.php';

// ========================================
// INPUT VALIDATION & SANITIZATION
// ========================================
$input = file_get_contents('php://input');
$data = json_decode($input, true);

// Check for valid JSON
if (json_last_error() !== JSON_ERROR_NONE) {
    sendErrorResponse('Invalid JSON format.', 400);
}

// Validate required fields
if (!isset($data['text']) || !isset($data['action'])) {
    sendErrorResponse('Missing required fields: text and action.', 400);
}

// Sanitize and validate input
$text = trim($data['text']);
$action = trim($data['action']);

// Validate text input
if (empty($text)) {
    sendErrorResponse('Text cannot be empty.', 400);
}

if (strlen($text) < 10) {
    sendErrorResponse('Text is too short. Minimum 10 characters required.', 400);
}

if (strlen($text) > 10000) {
    sendErrorResponse('Text is too long. Maximum 10000 characters allowed.', 400);
}

// Validate action
$validActions = ['summarize', 'reply', 'bullets'];
if (!in_array($action, $validActions)) {
    sendErrorResponse('Invalid action. Allowed values: summarize, reply, bullets.', 400);
}

// ========================================
// AI AUTOMATION LOGIC
// ========================================
try {
    // Build AI prompt based on action
    $prompt = buildPrompt($action, $text);
    
    // Call AI API
    $result = callAiAPI($prompt);
    
    // Log successful request
    logRequest($action, strlen($text), 'success');
    
    // Send success response
    sendSuccessResponse($result);
    
} catch (Exception $e) {
    // Log error
    logRequest($action, strlen($text), 'error: ' . $e->getMessage());
    
    // Send error response
    sendErrorResponse('AI processing failed: ' . $e->getMessage(), 500);
}

// ========================================
// FUNCTION: BUILD AI PROMPT
// ========================================
function buildPrompt($action, $text) {
    $prompts = [
        'summarize' => "Summarize the following text in a concise and clear manner:\n\n",
        'reply' => "Generate a professional and polite reply for the following message:\n\n",
        'bullets' => "Convert the following text into clear bullet points:\n\n"
    ];
    
    return $prompts[$action] . $text;
}

// ========================================
// FUNCTION: CALL AI API
// ========================================
function callAiAPI($prompt) {
    global $apiKey, $apiEndpoint;
    
    // Check if API key is configured
    if (empty($apiKey) || $apiKey === 'your-openai-api-key-here') {
        // Fallback to dummy response for testing
        return getDummyResponse($prompt);
    }
    
    // Prepare API request
    $data = [
        'model' => 'gpt-3.5-turbo',
        'messages' => [
            [
                'role' => 'system',
                'content' => 'You are a helpful assistant that provides concise and accurate responses.'
            ],
            [
                'role' => 'user',
                'content' => $prompt
            ]
        ],
        'max_tokens' => 500,
        'temperature' => 0.7
    ];
    
    // Initialize cURL
    $ch = curl_init($apiEndpoint);
    
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => [
            'Content-Type: application/json',
            'Authorization: Bearer ' . $apiKey
        ],
        CURLOPT_POSTFIELDS => json_encode($data),
        CURLOPT_TIMEOUT => 30,
        CURLOPT_SSL_VERIFYPEER => true
    ]);
    
    // Execute request
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    
    curl_close($ch);
    
    // Handle cURL errors
    if ($error) {
        throw new Exception('API request failed: ' . $error);
    }
    
    // Handle HTTP errors
    if ($httpCode !== 200) {
        throw new Exception('API returned error code: ' . $httpCode);
    }
    
    // Parse response
    $result = json_decode($response, true);
    
    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception('Invalid API response format.');
    }
    
    // Extract content from response
    if (isset($result['choices'][0]['message']['content'])) {
        return trim($result['choices'][0]['message']['content']);
    }
    
    throw new Exception('No content in API response.');
}

// ========================================
// FUNCTION: DUMMY RESPONSE (FALLBACK)
// ========================================
function getDummyResponse($prompt) {
    // This is a fallback for testing when API key is not configured
    // In production, this should be removed or disabled
    
    if (strpos($prompt, 'Summarize') !== false) {
        return "This is a summary of your text. The main points have been condensed into a brief overview that captures the essential information while maintaining clarity and coherence.";
    }
    
    if (strpos($prompt, 'reply') !== false) {
        return "Thank you for your message. I appreciate you taking the time to reach out. I've reviewed your input and wanted to provide a thoughtful and professional response. Please let me know if you need any additional information or clarification.";
    }
    
    if (strpos($prompt, 'bullet') !== false) {
        return "• Main point from your text has been identified\n• Key information has been extracted and organized\n• Content is presented in clear, concise bullet points\n• Easy to read and understand format\n• Professional presentation of information";
    }
    
    return "Your text has been processed successfully.";
}

// ========================================
// FUNCTION: LOG REQUEST
// ========================================
function logRequest($action, $textLength, $status) {
    $logFile = 'logs.txt';
    $timestamp = date('Y-m-d H:i:s');
    $ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    
    $logEntry = sprintf(
        "[%s] IP: %s | Action: %s | Text Length: %d | Status: %s\n",
        $timestamp,
        $ip,
        $action,
        $textLength,
        $status
    );
    
    // Append to log file
    file_put_contents($logFile, $logEntry, FILE_APPEND | LOCK_EX);
}

// ========================================
// FUNCTION: SEND SUCCESS RESPONSE
// ========================================
function sendSuccessResponse($data) {
    http_response_code(200);
    echo json_encode([
        'status' => 'success',
        'data' => $data,
        'timestamp' => time()
    ], JSON_PRETTY_PRINT);
    exit();
}

// ========================================
// FUNCTION: SEND ERROR RESPONSE
// ========================================
function sendErrorResponse($message, $code = 400) {
    http_response_code($code);
    echo json_encode([
        'status' => 'error',
        'message' => $message,
        'timestamp' => time()
    ], JSON_PRETTY_PRINT);
    exit();
}
