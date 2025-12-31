# Netlify Deployment Guide for Tetra Pak Dashboard

## What's Been Set Up

Your dashboard is now ready to deploy to Netlify! Here's what was configured:

1. **index.html** - Your main dashboard (renamed from dashboard.html)
2. **tetra_pak_data.json** - Your 23MB data file (configured to be included in git)
3. **netlify.toml** - Netlify configuration with:
   - Security headers
   - Proper caching for JSON data
   - SPA routing support

## Deploy to Netlify

### Option 1: Deploy via Git (Recommended)

1. **Commit your changes to git:**
   ```bash
   git add .
   git commit -m "Prepare dashboard for Netlify deployment"
   git push
   ```

2. **Connect to Netlify:**
   - Go to [netlify.com](https://netlify.com) and sign in
   - Click "Add new site" → "Import an existing project"
   - Choose your Git provider (GitHub, GitLab, or Bitbucket)
   - Select this repository
   - Netlify will automatically detect the settings from `netlify.toml`
   - Click "Deploy site"

### Option 2: Drag & Drop Deploy

1. **Go to Netlify:**
   - Visit [app.netlify.com/drop](https://app.netlify.com/drop)

2. **Drag these files into the drop zone:**
   - index.html
   - tetra_pak_data.json
   - netlify.toml (optional but recommended)

3. **Done!** Your site will be live in seconds.

## Important Notes

- **Data File Size:** Your JSON file is 23MB. Netlify supports this, but initial load time may take a few seconds
- **HTTPS:** Netlify provides free HTTPS automatically
- **Custom Domain:** You can add a custom domain in Netlify settings
- **Git Tracking:** The data file is now included in git (excluded other JSON files)

## What's Next?

After deployment:
- Test your dashboard at the provided Netlify URL
- Set up a custom domain (optional)
- Enable continuous deployment (updates automatically when you push to git)

## Files Structure

```
/
├── index.html              # Main dashboard
├── tetra_pak_data.json     # Data source (23MB)
├── netlify.toml            # Netlify configuration
└── .gitignore              # Updated to include tetra_pak_data.json
```

## Troubleshooting

**If data doesn't load:**
- Check browser console for errors
- Verify tetra_pak_data.json is in the root directory
- Ensure file permissions are correct

**If charts don't display:**
- Clear browser cache
- Check that Chart.js CDN is accessible
- Verify index.html loaded completely

## Performance Tips

- First load may take 3-5 seconds due to 23MB data file
- After first load, browsers will cache the data
- Consider adding a loading animation (already included in your dashboard)
