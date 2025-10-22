# Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the Mushroom ETL Pipeline.

## 📋 Table of Contents

- [Common Issues](#common-issues)
- [Error Messages](#error-messages)
- [Debugging Tools](#debugging-tools)
- [Performance Issues](#performance-issues)
- [Database Issues](#database-issues)
- [File System Issues](#file-system-issues)
- [Network Issues](#network-issues)
- [Logging and Monitoring](#logging-and-monitoring)

## Common Issues

### 1. Import Errors

**Problem**: `ModuleNotFoundError: No module named 'pandas'`

**Solution**:
```bash
# Check if virtual environment is activated
which python

# Install missing dependencies
pip install -r requirements.txt

# If specific package fails, install individually
pip install pandas numpy scikit-learn
```

**Problem**: `ModuleNotFoundError: No module named 'src'`

**Solution**:
```bash
# Add src to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Or run from project root
cd /path/to/mushroom_etl_project
python scripts/run_complete_etl.py
```

### 2. Database Connection Issues

**Problem**: `sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) unable to open database file`

**Solution**:
```bash
# Check database file permissions
ls -la data/mushroom_etl.db

# Create data directory if it doesn't exist
mkdir -p data

# Check database URL in configuration
echo $DATABASE_URL

# Test database connection
python -c "from sqlalchemy import create_engine; engine = create_engine('sqlite:///data/mushroom_etl.db'); print('Connection successful')"
```

**Problem**: `sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (127.0.0.1), port 5432 failed`

**Solution**:
```bash
# Check PostgreSQL service
sudo systemctl status postgresql

# Start PostgreSQL service
sudo systemctl start postgresql

# Check connection parameters
echo $DATABASE_URL

# Test connection
psql -h localhost -U username -d database_name
```

### 3. File System Issues

**Problem**: `FileNotFoundError: [Errno 2] No such file or directory: 'data/raw/mushroom_data.csv'`

**Solution**:
```bash
# Check if data directory exists
ls -la data/

# Create missing directories
mkdir -p data/raw data/processed data/models logs

# Check file permissions
ls -la data/raw/

# Set proper permissions
chmod 755 data/
chmod 644 data/raw/*
```

**Problem**: `PermissionError: [Errno 13] Permission denied: 'data/processed/output.parquet'`

**Solution**:
```bash
# Check directory permissions
ls -la data/processed/

# Fix permissions
chmod 755 data/processed/
chmod 644 data/processed/*

# Check if running as correct user
whoami
```

### 4. Memory Issues

**Problem**: `MemoryError: Unable to allocate array`

**Solution**:
```bash
# Check available memory
free -h

# Reduce batch size in configuration
export BATCH_SIZE=100

# Use chunking for large datasets
python scripts/run_complete_etl.py --chunk-size 1000

# Monitor memory usage
htop
```

**Problem**: `pandas.errors.MemoryError: Unable to allocate memory`

**Solution**:
```python
# Use chunking for large files
import pandas as pd

# Process in chunks
chunk_size = 1000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    # Process chunk
    process_chunk(chunk)
```

## Error Messages

### 1. Extraction Errors

**Error**: `requests.exceptions.ConnectionError: HTTPSConnectionPool(host='archive.ics.uci.edu', port=443)`

**Diagnosis**: Network connectivity issue
**Solution**:
```bash
# Test network connectivity
ping archive.ics.uci.edu

# Check if URL is accessible
curl -I https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data

# Try with different timeout
python scripts/run_complete_etl.py --timeout 60
```

**Error**: `pandas.errors.EmptyDataError: No columns to parse from file`

**Diagnosis**: Empty or corrupted data file
**Solution**:
```bash
# Check file content
head -5 data/raw/mushroom_data.csv

# Check file size
ls -la data/raw/mushroom_data.csv

# Re-download data
python scripts/download_data.py --force
```

### 2. Transformation Errors

**Error**: `ValueError: Input contains NaN, infinity or a value too large for dtype('float64')`

**Diagnosis**: Invalid data values
**Solution**:
```python
# Check for missing values
import pandas as pd
df = pd.read_csv('data/raw/mushroom_data.csv')
print(df.isnull().sum())

# Handle missing values
df = df.dropna()  # or df.fillna(method='ffill')
```

**Error**: `sklearn.exceptions.NotFittedError: This StandardScaler instance is not fitted yet`

**Diagnosis**: Transformer not fitted before transform
**Solution**:
```python
# Fit transformer before transform
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(X_train)
X_scaled = scaler.transform(X_test)
```

### 3. Loading Errors

**Error**: `sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed`

**Diagnosis**: Duplicate data in database
**Solution**:
```python
# Check for duplicates
import pandas as pd
df = pd.read_csv('data/processed/mushroom_data.csv')
print(df.duplicated().sum())

# Remove duplicates
df = df.drop_duplicates()
```

**Error**: `pandas.errors.ParserError: Error tokenizing data`

**Diagnosis**: Malformed CSV file
**Solution**:
```python
# Check CSV format
import pandas as pd

# Try different separators
df = pd.read_csv('file.csv', sep=';')
df = pd.read_csv('file.csv', sep='\t')

# Check encoding
df = pd.read_csv('file.csv', encoding='utf-8')
df = pd.read_csv('file.csv', encoding='latin-1')
```

## Debugging Tools

### 1. Logging Configuration

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Or set environment variable
export LOG_LEVEL=DEBUG
```

### 2. Pipeline Debug Mode

```bash
# Run pipeline in debug mode
python scripts/run_complete_etl.py --debug

# Enable verbose output
python scripts/run_complete_etl.py --verbose

# Run specific stage only
python scripts/run_complete_etl.py --stage extraction
```

### 3. Data Validation

```python
# Validate data at each stage
from src.utils.validation import validate_data

# Check data quality
quality_report = validate_data(df)
print(quality_report)
```

### 4. Performance Profiling

```python
# Profile pipeline performance
import cProfile
import pstats

# Run with profiling
cProfile.run('pipeline.run_pipeline()', 'profile_output.prof')

# Analyze results
stats = pstats.Stats('profile_output.prof')
stats.sort_stats('cumulative').print_stats(10)
```

## Performance Issues

### 1. Slow Pipeline Execution

**Symptoms**: Pipeline takes too long to complete
**Diagnosis**: Check CPU and memory usage
**Solution**:
```bash
# Monitor system resources
htop
iostat -x 1

# Optimize configuration
export MAX_WORKERS=4
export BATCH_SIZE=1000
export CHUNK_SIZE=10000
```

### 2. High Memory Usage

**Symptoms**: Out of memory errors
**Diagnosis**: Large datasets or memory leaks
**Solution**:
```python
# Use chunking
import pandas as pd

for chunk in pd.read_csv('large_file.csv', chunksize=1000):
    process_chunk(chunk)

# Clear memory
import gc
gc.collect()
```

### 3. Database Performance

**Symptoms**: Slow database operations
**Diagnosis**: Missing indexes or large tables
**Solution**:
```sql
-- Create indexes
CREATE INDEX idx_class ON mushroom_data(class);
CREATE INDEX idx_feature1 ON mushroom_data(feature1);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM mushroom_data WHERE class = 'e';
```

## Database Issues

### 1. Connection Pool Exhaustion

**Problem**: `sqlalchemy.exc.TimeoutError: QueuePool limit of size 5 overflow 10 reached`

**Solution**:
```python
# Increase pool size
from sqlalchemy import create_engine

engine = create_engine(
    'sqlite:///data/mushroom_etl.db',
    pool_size=20,
    max_overflow=30,
    pool_timeout=30
)
```

### 2. Lock Timeout

**Problem**: `sqlite3.OperationalError: database is locked`

**Solution**:
```python
# Use WAL mode for SQLite
import sqlite3

conn = sqlite3.connect('data/mushroom_etl.db')
conn.execute('PRAGMA journal_mode=WAL')
conn.close()
```

### 3. Transaction Issues

**Problem**: `sqlalchemy.exc.IntegrityError: transaction rollback`

**Solution**:
```python
# Use transactions properly
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

try:
    # Database operations
    session.commit()
except Exception as e:
    session.rollback()
    raise e
finally:
    session.close()
```

## File System Issues

### 1. Disk Space

**Problem**: `OSError: [Errno 28] No space left on device`

**Solution**:
```bash
# Check disk space
df -h

# Clean up old files
find data/ -name "*.tmp" -delete
find logs/ -name "*.log" -mtime +30 -delete

# Compress old data
gzip data/processed/old_data.csv
```

### 2. File Permissions

**Problem**: `PermissionError: [Errno 13] Permission denied`

**Solution**:
```bash
# Check file permissions
ls -la data/

# Fix permissions
chmod 755 data/
chmod 644 data/raw/*
chmod 644 data/processed/*

# Check ownership
ls -la data/
chown -R user:group data/
```

### 3. File Corruption

**Problem**: `pandas.errors.ParserError: Error tokenizing data`

**Solution**:
```bash
# Check file integrity
file data/raw/mushroom_data.csv

# Verify file size
ls -la data/raw/mushroom_data.csv

# Re-download if corrupted
python scripts/download_data.py --force
```

## Network Issues

### 1. Connection Timeout

**Problem**: `requests.exceptions.ConnectTimeout: HTTPSConnectionPool`

**Solution**:
```python
# Increase timeout
import requests

response = requests.get(url, timeout=60)

# Or configure in extractor
extractor = UCIMushroomExtractor(config={'timeout': 60})
```

### 2. SSL Certificate Issues

**Problem**: `requests.exceptions.SSLError: SSL: CERTIFICATE_VERIFY_FAILED`

**Solution**:
```python
# Disable SSL verification (not recommended for production)
import requests
requests.get(url, verify=False)

# Or update certificates
# On macOS:
# /Applications/Python\ 3.x/Install\ Certificates.command
```

### 3. Proxy Issues

**Problem**: `requests.exceptions.ProxyError: HTTPSConnectionPool`

**Solution**:
```python
# Configure proxy
import requests

proxies = {
    'http': 'http://proxy.company.com:8080',
    'https': 'https://proxy.company.com:8080'
}
response = requests.get(url, proxies=proxies)
```

## Logging and Monitoring

### 1. Log Analysis

```bash
# View recent logs
tail -f logs/etl_pipeline.log

# Search for errors
grep "ERROR" logs/etl_pipeline.log

# Search for specific stage
grep "extraction" logs/etl_pipeline.log

# Count errors
grep -c "ERROR" logs/etl_pipeline.log
```

### 2. Performance Monitoring

```bash
# Monitor pipeline performance
python scripts/monitor_pipeline.py

# Check pipeline health
python scripts/check_pipeline_health.py

# View pipeline statistics
python scripts/view_pipeline_stats.py
```

### 3. Alert Configuration

```python
# Set up alerts for critical errors
import logging
from logging.handlers import SMTPHandler

# Email alerts for errors
smtp_handler = SMTPHandler(
    mailhost='smtp.company.com',
    fromaddr='alerts@company.com',
    toaddrs=['admin@company.com'],
    subject='ETL Pipeline Error'
)
smtp_handler.setLevel(logging.ERROR)
logger.addHandler(smtp_handler)
```

## 🚨 Emergency Procedures

### 1. Pipeline Failure Recovery

```bash
# Stop running pipeline
pkill -f "run_complete_etl.py"

# Check pipeline status
python scripts/check_pipeline_health.py

# Restart pipeline
python scripts/run_complete_etl.py --mode production
```

### 2. Data Recovery

```bash
# Restore from backup
python scripts/restore_database.py --backup-file backup_20231201.db

# Restore files
python scripts/restore_files.py --backup-dir backup/20231201/
```

### 3. System Recovery

```bash
# Check system resources
htop
df -h
free -h

# Restart services
sudo systemctl restart postgresql
sudo systemctl restart nginx

# Clear caches
sync
echo 3 > /proc/sys/vm/drop_caches
```

## 📞 Getting Help

### 1. Self-Diagnosis

```bash
# Run diagnostic script
python scripts/diagnose_pipeline.py

# Generate system report
python scripts/generate_report.py
```

### 2. Log Collection

```bash
# Collect logs for support
tar -czf logs_$(date +%Y%m%d).tar.gz logs/
tar -czf config_$(date +%Y%m%d).tar.gz config/
```

### 3. Support Channels

- **Documentation**: Check this troubleshooting guide
- **Logs**: Review log files for error messages
- **Community**: GitHub issues and discussions
- **Support**: Contact support team with logs and error messages

## 🔧 Prevention

### 1. Regular Maintenance

```bash
# Daily maintenance
python scripts/daily_maintenance.py

# Weekly cleanup
python scripts/weekly_cleanup.py

# Monthly optimization
python scripts/monthly_optimization.py
```

### 2. Monitoring Setup

```bash
# Set up monitoring
python scripts/setup_monitoring.py

# Configure alerts
python scripts/configure_alerts.py

# Test monitoring
python scripts/test_monitoring.py
```

### 3. Backup Strategy

```bash
# Set up automated backups
crontab -e

# Add backup schedule
0 2 * * * /path/to/backup_script.sh
0 14 * * * /path/to/backup_script.sh
```
