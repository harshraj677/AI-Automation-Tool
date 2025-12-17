# 🤖 Smart Text Assistant - Mini AI Automation Tool

A professional, production-ready web application that leverages AI to automate text processing tasks. Built for the **Dinzin Developer Intern (PHP & JavaScript)** technical assignment.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![PHP](https://img.shields.io/badge/PHP-8.x-purple.svg)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)

---

## 📋 Overview

**Smart Text Assistant** is a web-based AI automation tool that helps users:
- **Summarize lengthy text** into concise overviews
- **Generate professional replies** to messages
- **Convert text into organized bullet points**

The application features a modern, responsive UI with real-time processing, error handling, and comprehensive logging.

---

## ✨ Features

### Core Functionality
- ✅ **Text Summarization** - Condense long text into brief summaries
- ✅ **Reply Generation** - Create professional, polite responses
- ✅ **Bullet Point Conversion** - Transform text into clear bullet lists

### Technical Features
- ✅ **Modern UI/UX** - Clean, professional design with smooth animations
- ✅ **Real-time Validation** - Client-side input validation with feedback
- ✅ **Loading States** - Visual feedback during processing
- ✅ **Error Handling** - Comprehensive error messages and logging
- ✅ **Copy to Clipboard** - One-click result copying
- ✅ **Character Counter** - Real-time character count display
- ✅ **Keyboard Shortcuts** - Ctrl/Cmd+Enter to submit, Escape to clear
- ✅ **Responsive Design** - Mobile-friendly interface
- ✅ **Request Logging** - Automatic logging of all requests
- ✅ **API Integration** - OpenAI API with fallback dummy responses

---

## 🛠️ Tech Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS variables and animations
- **JavaScript (ES6+)** - Vanilla JS with Fetch API

### Backend
- **PHP 7.4+** - Server-side processing
- **cURL** - External API communication

### API
- **OpenAI API** - AI text processing
- **Fallback System** - Dummy responses for testing without API key

---

## 📁 Project Structure

```
smart-text-assistant/
│
├── index.html          # Main application interface
├── style.css           # Stylesheet with modern design
├── script.js           # Frontend logic and API communication
├── api.php             # Backend API endpoint
├── config.php          # Configuration and API keys
├── logs.txt            # Request logging file
└── README.md           # Project documentation
```

---

## 🚀 Setup Instructions

### Prerequisites
- **PHP 7.4 or higher**
- **Web server** (Apache, Nginx, or PHP built-in server)
- **OpenAI API key** (optional - works with dummy responses)

### Installation Steps

#### 1. Clone or Download the Project
```bash
cd your-web-directory
# Place all project files in the directory
```

#### 2. Configure API Key (Optional but Recommended)
Open `config.php` and add your OpenAI API key:

```php
$apiKey = 'sk-your-actual-api-key-here';
```

**Get your API key:** [OpenAI API Keys](https://platform.openai.com/api-keys)

> **Note:** The application works without an API key using dummy responses for testing purposes.

#### 3. Set File Permissions (Linux/Mac)
```bash
chmod 644 config.php
chmod 666 logs.txt
```

#### 4. Start the Application

**Option A: Using PHP Built-in Server (Recommended for Testing)**
```bash
php -S localhost:8000
```

**Option B: Using Apache/Nginx**
- Place files in your web root directory (e.g., `/var/www/html/` or `htdocs/`)
- Access via: `http://localhost/smart-text-assistant/`

#### 5. Open in Browser
Navigate to:
```
http://localhost:8000
```
or your configured web server URL.

---

## 📖 Usage Guide

### Basic Workflow
1. **Enter text** in the text area (minimum 10 characters)
2. **Select an action** from the dropdown:
   - Summarize Text
   - Generate Professional Reply
   - Convert to Bullet Points
3. **Click "Process Text"** or press `Ctrl/Cmd + Enter`
4. **View results** in the output section
5. **Copy results** using the copy button

### Keyboard Shortcuts
- `Ctrl/Cmd + Enter` - Submit form
- `Escape` - Clear form and hide output

---

## 🔒 Security Features

- ✅ Input sanitization and validation
- ✅ API key stored in separate config file
- ✅ CORS headers configured
- ✅ Method validation (POST only)
- ✅ Error messages don't expose sensitive information
- ✅ Request logging with IP tracking

### Security Recommendations
1. **Never commit** `config.php` with real API keys to Git
2. Add `config.php` to `.gitignore`
3. Use environment variables in production:
   ```php
   $apiKey = getenv('OPENAI_API_KEY');
   ```
4. Set proper file permissions on production server
5. Enable HTTPS in production

---

## 📝 API Documentation

### Endpoint: `api.php`

**Method:** `POST`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "text": "Your text here",
  "action": "summarize|reply|bullets"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "data": "Processed AI output...",
  "timestamp": 1702819200
}
```

**Error Response (400/500):**
```json
{
  "status": "error",
  "message": "Error description",
  "timestamp": 1702819200
}
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** "API request failed"
- **Solution:** Check your API key in `config.php`
- **Solution:** Verify internet connection
- **Solution:** Check OpenAI API status

**Issue:** "No output displayed"
- **Solution:** Check browser console for errors
- **Solution:** Verify PHP error logs
- **Solution:** Ensure `logs.txt` is writable

**Issue:** "CORS errors"
- **Solution:** Ensure frontend and backend are on same domain
- **Solution:** Check CORS headers in `api.php`

**Issue:** Styling not loading
- **Solution:** Clear browser cache
- **Solution:** Check file paths in `index.html`

---

## 🧪 Testing

### Without API Key (Dummy Mode)
1. Leave API key as `'your-openai-api-key-here'` in `config.php`
2. Application will use fallback dummy responses
3. Perfect for testing UI/UX without API costs

### With API Key (Production Mode)
1. Add valid OpenAI API key to `config.php`
2. Test all three actions
3. Monitor `logs.txt` for request logging
4. Check API usage in OpenAI dashboard

---

## 📊 Logging

All requests are logged to `logs.txt` with the following format:
```
[YYYY-MM-DD HH:MM:SS] IP: xxx.xxx.xxx.xxx | Action: action_name | Text Length: number | Status: status
```

**Example:**
```
[2025-12-17 14:30:45] IP: 192.168.1.100 | Action: summarize | Text Length: 450 | Status: success
[2025-12-17 14:31:20] IP: 192.168.1.100 | Action: reply | Text Length: 180 | Status: success
```

---

## 🎨 Customization

### Change Color Scheme
Edit CSS variables in `style.css`:
```css
:root {
    --primary-color: #6366f1;  /* Change to your color */
    --primary-hover: #4f46e5;
    /* ... other variables */
}
```

### Modify AI Behavior
Edit prompts in `api.php`:
```php
$prompts = [
    'summarize' => "Your custom prompt here...",
    // ... other actions
];
```

### Add New Actions
1. Add option in `index.html`
2. Update validation in `script.js`
3. Add prompt in `api.php`
4. Update `config.php` constants

---

## 🚀 Deployment

### Production Checklist
- [ ] Add real OpenAI API key
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS
- [ ] Set proper file permissions
- [ ] Configure production web server
- [ ] Set up error logging
- [ ] Add rate limiting
- [ ] Implement API key rotation
- [ ] Set up monitoring
- [ ] Add `.gitignore` for sensitive files

### Recommended `.gitignore`
```
config.php
logs.txt
.env
*.log
```

---

## 🔮 Future Improvements

- [ ] User authentication system
- [ ] Rate limiting per user/IP
- [ ] Support for multiple AI providers
- [ ] Text language detection
- [ ] Translation feature
- [ ] History of processed requests
- [ ] Export results to PDF
- [ ] Batch processing
- [ ] Admin dashboard
- [ ] API usage analytics

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Developer Intern Candidate**  
Built for Dinzin Developer Intern Assignment  
Date: December 2025

---

## 🙏 Acknowledgments

- OpenAI for providing the AI API
- Dinzin for the assignment opportunity
- Modern web development community for best practices

---

## 📞 Support

For issues or questions:
1. Check the **Troubleshooting** section
2. Review **logs.txt** for errors
3. Verify **API configuration**
4. Test with **dummy responses** first

---

## ⭐ Project Highlights

This project demonstrates:
- ✅ Clean, modular code architecture
- ✅ Professional UI/UX design principles
- ✅ Proper error handling and validation
- ✅ Security best practices
- ✅ RESTful API design
- ✅ Comprehensive documentation
- ✅ Production-ready code quality

**Ready for deployment and portfolio showcase!**

---

**Made with ❤️ for the Dinzin Developer Intern Assignment**
