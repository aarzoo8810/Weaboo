from django import forms


class DateInput(forms.DateInput):
    input_type = "date"

class BrowseAnimeForm(forms.Form):
    limit = forms.IntegerField(
        initial=25, min_value=1, max_value=25, required=False)
    q = forms.CharField(label="Search" ,widget=forms.TextInput(attrs={'placeholder': 'Search'}), max_length=120, required=False)
    type = forms.ChoiceField(choices=(("", "Choose Type"),
                                      ("tv", "TV"),
                                      ("movie", "Movies"),
                                      ("ova", "OVA"),
                                      ("special", "Special"),
                                      ("ona", "ONA"),
                                      ("music", "Music")),
                                      required=False
                                      )
    score = forms.FloatField(min_value=0, max_value=10, required=False)
    min_score = forms.FloatField(label="Min Score", min_value=0, max_value=10, required=False)
    max_score = forms.FloatField(label="Max Score", min_value=0, max_value=10, required=False)
    status = forms.ChoiceField(choices=(("", "Choose Status"),
                                        ("airing", "On Air"),
                                        ("complete", "Complete"),
                                        ("upcoming", "Upcoming")),
                               required=False)
    rating = forms.ChoiceField(initial="Hell",choices=[("", "Choose Rating"),
                                                       ("g", "G- All Ages"),
                                        ("pg", "PG- Children"),
                                        ("pg13", "PG- Children"),
                                        ("r17", "R- 17+ (Violence & profanity)"),
                                        ("r", "R+- Mild Nudity"),
                                        ("rx", "Hentai")],
                                        required=False)
    #sfw = forms.ChoiceField(widget=forms.CheckboxInput, required=False)

    order_by = forms.ChoiceField(choices=[("", "Order By"),
                                          ("title", "Title"),
                                          ("start_date", "Start Date"),
                                          ("end_date", "End Date"),
                                          ("episodes", "Episodes"),
                                          ("score", "Score"),
                                          ("rank", "Rank"),
                                          ("popularity", "Popularity"),
                                          ("members", "Members"),
                                          ("favorites", "Favorites")],
                                            required=False,
                                            label="Order By")

    sort = forms.ChoiceField(choices=(("", "Sort By"),
                                      ("desc", "Descending"),
                                      ("asc", "Ascending")),
                                      required=False)
    start_date = forms.DateField(widget=DateInput, required=False)
    end_date = forms.DateField(widget=DateInput, required=False)

    class Meta:
        fields = "__all__"
        labels = {
            "limit": "Limit",
            "type": "Type",
            "score": "Score",
            "q": "Search",
            "min_score": "Min Score",
            "max_score": "Max Score",
            "status": "Status",
            "rating": "Rating",
            "order_by": "Order By",
            "start_date": "Start Date",
            "end_date": "End Date"
        }