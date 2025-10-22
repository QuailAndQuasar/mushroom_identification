# Production Deployment Guide

This guide covers deploying the Mushroom ETL Pipeline to production environments.

## 🚀 Production Deployment

### Prerequisites
- Python 3.10+
- Virtual environment
- Database (SQLite, PostgreSQL, MySQL)
- File storage (local, S3, GCS)
- Monitoring system (optional)

### Environment Setup

#### 1. Production Environment
```bash
# Create production environment
python -m venv venv_production
source venv_production/bin/activate

# Install production dependencies
pip install -r requirements.txt

# Set production environment variables
export ENVIRONMENT=production
export LOG_LEVEL=INFO
export DATABASE_URL=sqlite:///data/mushroom_etl_production.db
```

#### 2. Configuration
```bash
# Copy production configuration
cp config/pipeline.yaml config/pipeline_production.yaml

# Edit production settings
vim config/pipeline_production.yaml
```

#### 3. Database Setup
```bash
# Initialize production database
python scripts/init_database.py --environment production

# Run database migrations
python scripts/migrate.py --environment production
```

### Deployment Options

#### Option 1: Direct Deployment
```bash
# Run pipeline directly
python scripts/run_complete_etl.py --mode production

# Run with monitoring
python scripts/run_complete_etl.py --mode production --monitor
```

#### Option 2: Docker Deployment
```bash
# Build Docker image
docker build -t mushroom-etl:latest .

# Run with Docker
docker run -d \
  --name mushroom-etl \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -e ENVIRONMENT=production \
  mushroom-etl:latest
```

#### Option 3: Kubernetes Deployment
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mushroom-etl
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mushroom-etl
  template:
    metadata:
      labels:
        app: mushroom-etl
    spec:
      containers:
      - name: mushroom-etl
        image: mushroom-etl:latest
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: DATABASE_URL
          value: "sqlite:///data/mushroom_etl.db"
        volumeMounts:
        - name: data-volume
          mountPath: /app/data
        - name: logs-volume
          mountPath: /app/logs
      volumes:
      - name: data-volume
        persistentVolumeClaim:
          claimName: mushroom-etl-data
      - name: logs-volume
        persistentVolumeClaim:
          claimName: mushroom-etl-logs
```

### Monitoring and Alerting

#### 1. Health Checks
```bash
# Check pipeline health
python scripts/check_pipeline_health.py

# Check database health
python scripts/check_database_health.py

# Check file system health
python scripts/check_filesystem_health.py
```

#### 2. Logging
```bash
# View pipeline logs
tail -f logs/etl_pipeline.log

# View error logs
grep "ERROR" logs/etl_pipeline.log

# View performance logs
grep "PERFORMANCE" logs/etl_pipeline.log
```

#### 3. Metrics
```bash
# View pipeline metrics
python scripts/view_pipeline_metrics.py

# Export metrics
python scripts/export_metrics.py --format json
```

### Performance Optimization

#### 1. Database Optimization
```sql
-- Create indexes for better performance
CREATE INDEX idx_class ON mushroom_data(class);
CREATE INDEX idx_feature1 ON mushroom_data(feature1);
CREATE INDEX idx_feature2 ON mushroom_data(feature2);
```

#### 2. File System Optimization
```bash
# Optimize file storage
python scripts/optimize_storage.py

# Compress old data
python scripts/compress_old_data.py
```

#### 3. Memory Optimization
```python
# Configure memory settings
import os
os.environ['PYTHONHASHSEED'] = '0'
os.environ['OMP_NUM_THREADS'] = '4'
```

### Security Considerations

#### 1. Environment Variables
```bash
# Secure environment variables
export DATABASE_PASSWORD="secure_password"
export API_KEY="secure_api_key"
export SECRET_KEY="secure_secret_key"
```

#### 2. File Permissions
```bash
# Set secure file permissions
chmod 600 .env
chmod 600 config/pipeline_production.yaml
chmod 755 scripts/
```

#### 3. Network Security
```bash
# Configure firewall rules
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw deny 3306/tcp
```

### Backup and Recovery

#### 1. Data Backup
```bash
# Backup database
python scripts/backup_database.py

# Backup files
python scripts/backup_files.py

# Automated backup
crontab -e
# Add: 0 2 * * * /path/to/backup_script.sh
```

#### 2. Recovery Procedures
```bash
# Restore database
python scripts/restore_database.py --backup-file backup.db

# Restore files
python scripts/restore_files.py --backup-dir backup/
```

### Troubleshooting

#### Common Issues
1. **Database Connection Issues**
   - Check database URL
   - Verify database permissions
   - Check network connectivity

2. **File System Issues**
   - Check disk space
   - Verify file permissions
   - Check file system health

3. **Performance Issues**
   - Monitor memory usage
   - Check CPU utilization
   - Review log files

#### Debug Mode
```bash
# Run in debug mode
python scripts/run_complete_etl.py --mode production --debug

# Enable verbose logging
export LOG_LEVEL=DEBUG
python scripts/run_complete_etl.py --mode production
```

### Maintenance

#### 1. Regular Maintenance
```bash
# Daily maintenance
python scripts/daily_maintenance.py

# Weekly maintenance
python scripts/weekly_maintenance.py

# Monthly maintenance
python scripts/monthly_maintenance.py
```

#### 2. Updates
```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Run migrations
python scripts/migrate.py

# Restart services
systemctl restart mushroom-etl
```

### Scaling

#### 1. Horizontal Scaling
```bash
# Run multiple instances
python scripts/run_complete_etl.py --instance 1
python scripts/run_complete_etl.py --instance 2
```

#### 2. Vertical Scaling
```bash
# Increase memory
export PYTHONHASHSEED=0
export OMP_NUM_THREADS=8
```

## 📊 Production Checklist

- [ ] Environment variables configured
- [ ] Database initialized and migrated
- [ ] File system permissions set
- [ ] Monitoring configured
- [ ] Logging configured
- [ ] Backup procedures in place
- [ ] Security measures implemented
- [ ] Performance optimization applied
- [ ] Health checks configured
- [ ] Documentation updated

## 🆘 Support

For production support:
- Check logs: `tail -f logs/etl_pipeline.log`
- Run health checks: `python scripts/check_pipeline_health.py`
- Review documentation: `docs/`
- Contact support: [support@example.com]