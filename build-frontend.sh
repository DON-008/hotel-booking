#!/bin/bash

# Build script for Netlify deployment
echo "🚀 Starting frontend build process..."

# Navigate to frontend directory
cd hotel-booking

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build the application
echo "🔨 Building Angular application..."
npm run build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build completed successfully!"
    echo "📁 Build output: dist/hotel-booking"
else
    echo "❌ Build failed!"
    exit 1
fi
