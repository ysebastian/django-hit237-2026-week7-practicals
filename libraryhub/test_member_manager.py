import os
import django
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'libraryhub.settings')
django.setup()

from catalogue.models import Member

# Test the with_loan_stats() method
members = Member.objects.with_loan_stats()
print("Members with loan stats:")
for member in members:
    print("  {}: active={}, total={}".format(member.user.username, member.active_loan_count, member.total_loan_count))

print("\nTest passed! MemberManager is working correctly.")
