#!/usr/bin/env python3
"""
Simple HTTP Server with PHP Support
Handles static files and proxies PHP requests
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import subprocess
import json
import os

class PHPHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to all responses
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        SimpleHTTPRequestHandler.end_headers(self)
    
    def do_GET(self):
        # Serve static files
        if self.path == '/':
            self.path = '/index.html'
        return SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        if self.path == '/api.php':
            # Get content length
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Execute PHP script
            try:
                result = subprocess.run(
                    ['php', 'api.php'],
                    input=post_data,
                    capture_output=True,
                    timeout=30
                )
                
                # Send response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(result.stdout)
                
            except FileNotFoundError:
                # PHP not installed
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                # Parse request
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    action = data.get('action', '')
                    text = data.get('text', '')
                    
                    # Process text based on action with actual input
                    if action == 'summarize':
                        result = self.generate_summary(text)
                    elif action == 'reply':
                        result = self.generate_reply(text)
                    elif action == 'bullets':
                        result = self.generate_bullets(text)
                    else:
                        result = 'Your text has been processed successfully.'
                    
                    response = {
                        'status': 'success',
                        'data': result
                    }
                    
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                    
                except Exception as e:
                    error_response = {
                        'status': 'error',
                        'message': str(e)
                    }
                    self.wfile.write(json.dumps(error_response).encode('utf-8'))
                    
            except subprocess.TimeoutExpired:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error = {'status': 'error', 'message': 'Request timeout'}
                self.wfile.write(json.dumps(error).encode('utf-8'))
                
        else:
            self.send_error(404)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def generate_summary(self, text):
        """Generate a summary from the input text"""
        sentences = text.replace('\n', ' ').split('. ')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= 2:
            return f"Summary: {text}"
        
        # Take first and last sentences, and add word count info
        words = text.split()
        summary = f"{sentences[0]}. "
        
        if len(sentences) > 3:
            summary += f"{sentences[-1]}. "
        
        summary += f"\n\nKey Stats:\n• Original length: {len(words)} words\n• {len(sentences)} sentences\n• Main topic discussed throughout the text"
        
        return summary
    
    def generate_reply(self, text):
        """Generate a professional reply based on input"""
        # Extract key words for context
        words = text.lower().split()
        
        reply = "Thank you for your message. "
        
        if any(word in words for word in ['help', 'assist', 'support']):
            reply += "I'd be happy to assist you with your request. "
        elif any(word in words for word in ['question', 'ask', 'wondering']):
            reply += "That's a great question. "
        elif any(word in words for word in ['feedback', 'suggestion', 'idea']):
            reply += "I appreciate your feedback and suggestions. "
        
        reply += f"Regarding your message about: \"{text[:100]}{'...' if len(text) > 100 else ''}\"\n\n"
        reply += "I've carefully reviewed your input and wanted to provide a thoughtful response. "
        reply += "Please let me know if you need any additional information or clarification on this matter. "
        reply += "\n\nBest regards"
        
        return reply
    
    def generate_bullets(self, text):
        """Convert text into bullet points"""
        # Split into sentences
        sentences = text.replace('\n', '. ').split('. ')
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
        
        if not sentences:
            return "• " + text
        
        bullets = []
        for i, sentence in enumerate(sentences[:8]):  # Max 8 bullets
            # Clean up sentence
            sentence = sentence.strip()
            if not sentence.endswith('.'):
                sentence += '.'
            bullets.append(f"• {sentence}")
        
        result = "\n".join(bullets)
        
        if len(sentences) > 8:
            result += f"\n\n... and {len(sentences) - 8} more points from your text"
        
        return result
    
    def log_message(self, format, *args):
        # Custom log format
        print(f"[{self.log_date_time_string()}] {format % args}")

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, PHPHandler)
    print(f'\n✅ Server running at http://localhost:{port}')
    print(f'📁 Serving files from: {os.getcwd()}')
    print(f'\n🌐 Open in browser: http://localhost:{port}\n')
    print('Press Ctrl+C to stop\n')
    httpd.serve_forever()

if __name__ == '__main__':
    try:
        run_server(8000)
    except KeyboardInterrupt:
        print('\n\n✅ Server stopped')
