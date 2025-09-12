# Deployment Guide

This guide covers deploying the Django Diary PWA to various platforms.

## Quick Deploy Options

### 1. Railway (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway new
railway add
railway deploy
```

### 2. Heroku

```bash
# Install Heroku CLI and login
heroku login
heroku create your-diary-app-name

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser (optional)
heroku run python manage.py createsuperuser
```

### 3. DigitalOcean App Platform

1. Fork this repository
2. Connect your GitHub account to DigitalOcean
3. Create new app from GitHub
4. Select this repository
5. DigitalOcean will auto-detect Django settings

## Environment Variables

Set these in your hosting platform:

```
DEBUG=False
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgres://user:pass@host:port/dbname
ALLOWED_HOSTS=yourdomain.com,*.yourdomain.com
```

## Database Setup

### SQLite (Default)
- Works out of the box
- Good for small to medium usage
- Included in repository

### PostgreSQL (Production)
- Recommended for production
- Set `DATABASE_URL` environment variable
- Migrations run automatically

## Static Files

The app uses WhiteNoise for static file serving, so no additional setup is needed for static files.

## SSL/HTTPS

For PWA features to work properly, you need HTTPS. Most hosting platforms provide this automatically.

## Post-Deployment Checklist

- [ ] App loads without errors
- [ ] User registration works
- [ ] PWA manifest loads (`/static/entries/manifest.json`)
- [ ] Service worker registers (check browser dev tools)
- [ ] App can be installed (look for install prompt)
- [ ] Offline functionality works

## Troubleshooting

### Common Issues

1. **Static files not loading**
   - Ensure `STATIC_ROOT` is set correctly
   - Run `python manage.py collectstatic`

2. **Database connection errors**
   - Check `DATABASE_URL` format
   - Ensure database exists and is accessible

3. **PWA not installing**
   - Verify HTTPS is enabled
   - Check manifest.json is accessible
   - Ensure service worker registers without errors

4. **Images not displaying**
   - Check `MEDIA_URL` and `MEDIA_ROOT` settings
   - Configure media file serving for production

### Debug Mode

Never set `DEBUG=True` in production. If you need to debug:

1. Check application logs
2. Use Django's logging framework
3. Test locally with `DEBUG=True` first

## Performance Tips

1. **Enable caching**
   ```python
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
           'LOCATION': 'cache_table',
       }
   }
   ```

2. **Optimize database queries**
   - Use `select_related()` and `prefetch_related()`
   - Add database indexes for frequently queried fields

3. **Compress static files**
   - Enable gzip compression on your server
   - Consider using a CDN for static files

## Monitoring

Consider adding:
- Error tracking (Sentry)
- Performance monitoring
- Uptime monitoring
- Database backup schedule

## Scaling

For high traffic:
1. Use Redis for caching and sessions
2. Implement database read replicas
3. Use a CDN for static files
4. Consider horizontal scaling with load balancers
