# Development Workflow

## Branch Strategy

### Main Branch (`main`)
- **Purpose**: Production-ready code only
- **When to commit**: Only when major features are complete and tested
- **Protection**: Should be protected from direct pushes
- **Content**: Stable, tested, and production-ready code

### Development Branch (`development`)
- **Purpose**: Active development and feature integration
- **When to commit**: All ongoing development work
- **Content**: Latest features, bug fixes, and experimental code
- **Merging**: Regular commits for development progress

## Workflow Process

### 1. Daily Development
```bash
# Always work on development branch
git checkout development

# Create feature branches for specific features
git checkout -b feature/your-feature-name

# Make your changes and commit
git add .
git commit -m "Add your feature description"

# Push feature branch
git push origin feature/your-feature-name

# Merge back to development
git checkout development
git merge feature/your-feature-name
git push origin development
```

### 2. Feature Development
- Create feature branches from `development`
- Work on features in isolation
- Merge back to `development` when feature is complete
- Delete feature branches after merging

### 3. Production Releases
```bash
# When major features are complete and tested
git checkout main
git merge development
git tag v1.0.0  # or appropriate version
git push origin main --tags
```

### 4. Hotfixes (if needed)
```bash
# For critical production issues
git checkout main
git checkout -b hotfix/critical-issue
# Fix the issue
git commit -m "Fix critical issue"
git checkout main
git merge hotfix/critical-issue
git push origin main
```

## Current Project Status

- **Current Branch**: `development`
- **Main Branch**: Clean and ready for production releases
- **Active Development**: All new features should be developed in `development` branch

## Best Practices

1. **Never commit directly to main** - Always go through development branch
2. **Test thoroughly** before merging to main
3. **Use descriptive commit messages**
4. **Keep development branch up to date** with regular commits
5. **Create feature branches** for larger features
6. **Review code** before merging to main

## File Structure

```
├── app.py                 # Main Flask application
├── templates/             # HTML templates
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── DEVELOPMENT_WORKFLOW.md # This file
└── .env.example          # Environment template
```

## Next Steps

1. Continue development in `development` branch
2. Commit regularly as features are completed
3. Merge to `main` only when major features are ready for production
4. Use this workflow for all future development