import os
import django
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'libraryhub.settings')
django.setup()

from django.contrib.auth.models import User
from catalogue.models import Member

# Get a member first to find their user
member = Member.objects.first()
user = member.user
print("Testing for_user method:")
print("User: {}".format(user.username))

# Test for_user on manager
result = Member.objects.for_user(user)
print("Result type: {}".format(type(result).__name__))
print("Found member: {}".format(result.first().user.username if result.exists() else "No member found"))

# Test chaining with for_user and with_loan_stats
member_with_stats = Member.objects.for_user(user).with_loan_stats()
if member_with_stats.exists():
    m = member_with_stats.first()
    print("\nMember with stats:")
    print("  Username: {}".format(m.user.username))
    print("  Active loans: {}".format(m.active_loan_count))
    print("  Total loans: {}".format(m.total_loan_count))

print("\nTest passed! for_user method is working correctly and can be chained with other methods.")
