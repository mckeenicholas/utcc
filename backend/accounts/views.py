from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from results.models import Competition, Result
from django import forms


class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ["name", "date"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ["name", "event", "round", "time1", "time2", "time3", "time4", "time5"]
        widgets = {
            "event": forms.Select(attrs={"class": "form-control"}),
            "round": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "time1": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Time in centiseconds"}
            ),
            "time2": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Time in centiseconds"}
            ),
            "time3": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Time in centiseconds"}
            ),
            "time4": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Time in centiseconds"}
            ),
            "time5": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Time in centiseconds"}
            ),
        }


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print("logged in")
                return redirect("accounts:dashboard")
            else:
                return render(
                    request, "accounts/login.html", {"error": "Invalid credentials"}
                )
        else:
            return render(
                request,
                "accounts/login.html",
                {"error": "Please provide both username and password"},
            )

    return render(request, "accounts/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("accounts:login")


@login_required
def dashboard(request):
    if request.method == "POST":
        form = CompetitionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:dashboard")
    else:
        form = CompetitionForm()

    competitions = Competition.objects.all().order_by("-date")
    return render(
        request, "accounts/dashboard.html", {"competitions": competitions, "form": form}
    )


@login_required
def competition_detail(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)

    if request.method == "POST":
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.competition = competition
            result.save()
            return redirect(
                "accounts:competition_detail", competition_id=competition_id
            )
    else:
        form = ResultForm()

    results = Result.objects.filter(competition=competition).order_by("event", "round")
    return render(
        request,
        "accounts/competition_detail.html",
        {"competition": competition, "form": form, "results": results},
    )
