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
                    
                    # Dummy responses
                    responses = {
                        'summarize': "This is a summary of your text. The main points have been condensed into a brief overview that captures the essential information while maintaining clarity and coherence.",
                        'reply': "Thank you for your message. I appreciate you taking the time to reach out. I've reviewed your input and wanted to provide a thoughtful and professional response. Please let me know if you need any additional information or clarification.",
                        'bullets': "• Main point from your text has been identified\n• Key information has been extracted and organized\n• Content is presented in clear, concise bullet points\n• Easy to read and understand format\n• Professional presentation of information"
                    }
                    
                    response = {
                        'status': 'success',
                        'data': responses.get(action, 'Your text has been processed successfully.')
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
