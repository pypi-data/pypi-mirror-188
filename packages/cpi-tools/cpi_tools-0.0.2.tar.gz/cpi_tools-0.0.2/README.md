# CPI Data Tools

A repository of commonly used tools across CPI

## Instructions

1. Install:

```
pip install cpi_tools
```

AWS Tools

```python
from cpi_tools import aws_tools

#S3 Bucket
afolu_bucket = 'cpi-afolu-landscape'
#Path within S3
path = 'entity_name_data'
#S3 File name 
file_name = 'afolu_entity_list.csv'

#Read file from S3
df = aws_tools.read_from_s3(afolu_bucket, path, file_name)
```

