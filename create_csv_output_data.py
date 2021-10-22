import csv

# csv header
fieldnames = ['company_id', 'fi_section', 'as_reported_label', 'normalization_labels']

# csv data
rows = [
    {'company': 'Albania',
     'fi_section': 28748,
     'as_reported_label': 'AL',
     'normalization_labels': 'ALB'},
    {'company': 'Algeria',
     'fi_section': 2381741,
     'as_reported_label': 'DZ',
     'normalization_labels': 'DZA'},
    {'company': 'American Samoa',
     'fi_section': 199,
     'as_reported_label': 'AS',
     'normalization_labels': 'ASM'}
]

with open('data.csv', 'w+', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
