# Sudoku Game - AWS Deployment

Interactive Sudoku web game with HTML, CSS, and JavaScript deployed on AWS.

## 🎮 Live Demo

- **S3 Website**: http://sudoku-game-1756950518.s3-website-us-east-1.amazonaws.com
- **CloudFront**: https://d10i28jiugsdtx.cloudfront.net
- **Custom Domain**: https://samplesrini.com (when configured)

## 🚀 Features

- Modern responsive design
- Visual feedback and animations
- Timer and progress tracking
- Mobile and desktop optimized
- Keyboard and mouse support
- Eye-strain reducing color scheme

## 🏗️ Architecture

- **Frontend**: HTML5, CSS3, JavaScript
- **Hosting**: Amazon S3 Static Website
- **CDN**: Amazon CloudFront
- **DNS**: Amazon Route53 (for custom domain)
- **Deployment**: GitHub Actions CI/CD

## 📦 Deployment

### Automatic Deployment
Push changes to `main` branch to trigger automatic deployment via GitHub Actions.

### Manual Deployment
```bash
# Deploy to S3
aws s3 cp sudoku.html s3://sudoku-game-1756950518/ --content-type "text/html"
aws s3 cp static/style.css s3://sudoku-game-1756950518/ --content-type "text/css"

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id E1LD984NTKN8WY --paths "/*"
```

## 🔧 Setup GitHub Actions

1. Add AWS credentials to GitHub Secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

2. Push changes to trigger deployment

## 📁 Project Structure

```
├── sudoku.html          # Main game file
├── static/
│   └── style.css        # Game styles
├── .github/
│   └── workflows/
│       └── deploy.yml   # CI/CD pipeline
├── sudoku_stack.py      # CDK infrastructure
└── README.md           # This file
```

## 🛠️ Local Development

1. Open `sudoku.html` in browser
2. Make changes to HTML/CSS
3. Push to GitHub for automatic deployment

## 📊 AWS Resources

- S3 Buckets: `sudoku-game-1756950518`, `sudoku-final-1756952030`
- CloudFront Distribution: `E1LD984NTKN8WY`
- Route53 Hosted Zone: `/hostedzone/Z00893923ERUMJ5TFJ02U`
