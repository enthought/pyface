# This is used to test what happens when there is an unrelated import error
# when importing a toolkit object

raise ImportError('No module named nonexistent')
