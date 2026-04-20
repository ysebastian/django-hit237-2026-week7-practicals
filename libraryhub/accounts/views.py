from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from catalogue.models import Member
from .forms import CustomUserCreationForm


class SignupView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        """Save User and create corresponding Member instance with selected membership type."""
        
        # Extract membership_type from form (not a User model field)
        membership_type = form.cleaned_data['membership_type']
        
        # Save User and set self.object
        self.object = form.save()
        
        # Create Member linked to the newly created User
        Member.objects.create(
            user=self.object,
            library_card_number=f"LIB-{self.object.pk:04d}",
            membership_type=membership_type
        )
        
        return super().form_valid(form)
