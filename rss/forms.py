from django import forms


class SearchForm(forms.Form):
    search_terms = forms.CharField(label="search terms", max_length=200)
