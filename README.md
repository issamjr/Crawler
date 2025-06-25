# 🕷️ Advanced Web Crawler

<div align="center">

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Version](https://img.shields.io/badge/version-2.0-orange.svg)
![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)

**A powerful, multi-threaded web crawler for domain exploration and link extraction**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Examples](#-examples) • [Contributing](#-contributing)

</div>

---

## 🎯 Overview

The Advanced Web Crawler is a sophisticated Python tool designed for comprehensive website exploration and link extraction. Built with performance and flexibility in mind, it supports multi-threading, depth control, robots.txt compliance, and various output formats.

### 🌟 Key Highlights

- **⚡ Multi-threaded**: Concurrent crawling for maximum speed
- **🛡️ Robots.txt Compliant**: Respects website crawling policies
- **📊 Real-time Statistics**: Live crawling metrics and progress
- **🎨 Colorful Output**: Beautiful terminal interface with status indicators
- **💾 Multiple Formats**: Export results in TXT or JSON format
- **🔍 Depth Control**: Configurable crawling depth limits
- **⏱️ Rate Limiting**: Built-in delays to prevent server overload
- **📝 Detailed Logging**: Comprehensive logging capabilities

---

## ✨ Features

### Core Functionality
- 🔗 **Link Extraction**: Discovers all internal links within a domain
- 🧵 **Multi-threading**: Concurrent processing for faster crawling
- 📈 **Progress Tracking**: Real-time status updates and statistics
- 🎯 **Domain Filtering**: Automatically filters links to stay within target domain

### Advanced Features
- 🤖 **Robots.txt Support**: Checks and respects robots.txt policies
- 📏 **Depth Control**: Set maximum crawling depth to limit scope
- ⏰ **Rate Limiting**: Configurable delays between requests
- 🎨 **Status Color Coding**: Visual indicators for different HTTP status codes
- 📊 **Comprehensive Stats**: Detailed crawling statistics and performance metrics

### Output & Logging
- 💾 **Multiple Output Formats**: Save results in TXT or JSON format
- 📝 **Detailed Logging**: Optional file logging for audit trails
- 🎨 **Beautiful Terminal UI**: ASCII banner and colored output
- 📈 **Performance Metrics**: Speed, success rate, and timing statistics

---

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Quick Install

1. **Clone the repository:**
   ```bash
   git clone https://github.com/issamjr/Crawler.git
   cd Crawler
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Manual Installation

If you prefer to install dependencies manually:

```bash
pip install requests beautifulsoup4 colorama
```

### Requirements File

Create a `requirements.txt` file with:
```
requests>=2.28.0
beautifulsoup4>=4.11.0
colorama>=0.4.6
```

---

## 📖 Usage

### Basic Syntax
```bash
python crawler.py <URL> [OPTIONS]
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--threads` | Number of concurrent threads | 10 |
| `-o, --output` | Output file path | None |
| `--format` | Output format (txt/json) | txt |
| `--depth` | Maximum crawling depth | Unlimited |
| `--delay` | Delay between requests (seconds) | 0 |
| `--timeout` | Request timeout (seconds) | 10 |
| `--user-agent` | Custom User-Agent string | Default browser UA |
| `--log` | Log file path | None |
| `--no-robots` | Ignore robots.txt | False |

---

## 💡 Examples

### Basic Crawling
```bash
# Simple crawl of a website
python crawler.py https://example.com
```

### Advanced Usage
```bash
# High-performance crawling with 20 threads
python crawler.py https://example.com --threads 20

# Limited depth crawling with output
python crawler.py https://example.com --depth 3 -o results.txt

# JSON output with logging
python crawler.py https://example.com -o results.json --format json --log crawler.log

# Rate-limited crawling (respectful)
python crawler.py https://example.com --delay 1 --threads 5

# Custom User-Agent with robots.txt ignored
python crawler.py https://example.com --user-agent "My Custom Bot 1.0" --no-robots
```

### Sample Output

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      🕷️  Advanced Web Crawler v2.0  🕷️                      ║
║                        Created by Issam Junior                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

🚀 Starting crawler for domain: example.com
⚙️  Configuration: 10 threads, 10s timeout
🔍 Maximum depth: 3
════════════════════════════════════════════════════════════════════════════════

[*] Checked robots.txt: https://example.com/robots.txt
[+] https://example.com [200] (15,234 bytes) [Depth: 0]
[+] https://example.com/about [200] (8,456 bytes) [Depth: 1]
[+] https://example.com/contact [200] (5,123 bytes) [Depth: 1]

════════════════════════════════════════════════════════════════════════════════
                              CRAWLING STATISTICS
════════════════════════════════════════════════════════════════════════════════
📊 Total unique links found: 47
📄 Total pages processed: 47
✅ Successful requests: 45
❌ Failed requests: 2
⏱️  Total crawling time: 12.34 seconds
⚡ Average speed: 3.81 pages/second
════════════════════════════════════════════════════════════════════════════════
```

---

## 📁 Output Formats

### Text Format
```
# Web Crawler Results
# Generated on: 2024-03-15 14:30:22
# Total links found: 47

https://example.com
https://example.com/about
https://example.com/contact
https://example.com/services
...
```

### JSON Format
```json
{
  "timestamp": "2024-03-15 14:30:22",
  "statistics": {
    "total_pages": 47,
    "successful_requests": 45,
    "failed_requests": 2,
    "robots_txt_checked": true
  },
  "links": [
    "https://example.com",
    "https://example.com/about",
    "https://example.com/contact"
  ]
}
```

---

## 🎨 Color Coding

The crawler uses intuitive color coding for different status types:

- 🟢 **Green**: Successful requests (200 OK)
- 🟡 **Yellow**: Redirects and client errors (3xx, 4xx)
- 🔴 **Red**: Server errors and timeouts (5xx, timeouts)
- 🔵 **Blue**: General information and URLs
- 🟣 **Magenta**: Depth progression and statistics
- 🟠 **Cyan**: File sizes and technical details

---

## ⚙️ Configuration

### Environment Variables
You can set default values using environment variables:

```bash
export CRAWLER_THREADS=20
export CRAWLER_TIMEOUT=15
export CRAWLER_DELAY=0.5
```

### Robots.txt Compliance
By default, the crawler respects robots.txt files. To check what's allowed:

1. The crawler automatically fetches `/robots.txt`
2. Checks permissions for each URL before crawling
3. Skips disallowed URLs with a warning message

---

## 🔧 Troubleshooting

### Common Issues

**1. SSL Certificate Errors**
```bash
# Solution: Use --no-verify-ssl flag (if available in future versions)
# Or install certificates: pip install --upgrade certifi
```

**2. High Memory Usage**
```bash
# Reduce threads and add delays
python crawler.py https://example.com --threads 5 --delay 1
```

**3. Rate Limiting by Target Site**
```bash
# Add delays and reduce threads
python crawler.py https://example.com --delay 2 --threads 3
```

**4. Permission Denied Errors**
```bash
# Check robots.txt or use --no-robots flag
python crawler.py https://example.com --no-robots
```

### Performance Tips

- **Optimal Thread Count**: Start with 10 threads, adjust based on performance
- **Respectful Crawling**: Use delays for busy sites (`--delay 1`)
- **Depth Limiting**: Use `--depth` to prevent infinite crawling
- **Output Management**: Use JSON format for programmatic processing

---

## 🛠️ Development

### Project Structure
```
Crawler/
├── crawler.py          # Main crawler script
├── requirements.txt    # Python dependencies
├── README.md          # Documentation
├── LICENSE            # License file
└── examples/          # Usage examples
    ├── basic.py       # Basic usage examples
    └── advanced.py    # Advanced configurations
```

### Code Quality
- **PEP 8 Compliant**: Follows Python style guidelines
- **Type Hints**: Modern Python typing for better code clarity
- **Error Handling**: Comprehensive exception handling
- **Documentation**: Detailed docstrings and comments

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute
- 🐛 **Bug Reports**: Report issues with detailed descriptions
- 💡 **Feature Requests**: Suggest new functionality
- 📝 **Documentation**: Improve or translate documentation
- 🔧 **Code Contributions**: Submit pull requests with improvements

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test them
4. Submit a pull request with a clear description

### Coding Guidelines
- Follow PEP 8 style guidelines
- Add type hints where appropriate
- Include docstrings for new functions
- Write tests for new features
- Update documentation as needed

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Issam Junior

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- **BeautifulSoup**: For excellent HTML parsing capabilities
- **Requests Library**: For reliable HTTP handling
- **Colorama**: For beautiful terminal colors
- **Python Community**: For continuous inspiration and support

---
### Stay Updated
- ⭐ **Star this repository** to stay updated with new releases
- 👀 **Watch** for notifications about new features and updates
- 🍴 **Fork** to create your own customized version

---

<div align="center">

**Made with ❤️ by [Issam Junior](https://github.com/issamjr)**

![Visitor Count](https://visitor-badge.laobi.icu/badge?page_id=issamjr.Crawler)
![GitHub Stars](https://img.shields.io/github/stars/issamjr/Crawler?style=social)
![GitHub Forks](https://img.shields.io/github/forks/issamjr/Crawler?style=social)

</div>
