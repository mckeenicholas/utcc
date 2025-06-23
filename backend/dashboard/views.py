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
        return redirect("dashboard:dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print("logged in")
                return redirect("dashboard:dashboard")
            else:
                return render(
                    request, "dashboard/login.html", {"error": "Invalid credentials"}
                )
        else:
            return render(
                request,
                "dashboard/login.html",
                {"error": "Please provide both username and password"},
            )

    return render(request, "dashboard/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("dashboard:login")


@login_required
def dashboard(request):
    if request.method == "POST":
        new_competition_form = CompetitionForm(request.POST)
        if new_competition_form.is_valid():
            new_competition_form.save()
            return redirect("dashboard:dashboard")
    else:
        new_competition_form = CompetitionForm()

    competitions = Competition.objects.all().order_by("-date")
    return render(
        request,
        "dashboard/home.html",
        {"competitions": competitions, "form": new_competition_form},
    )


@login_required
def competition_detail(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)

    if request.method == "POST":
        results_form = ResultForm(request.POST)
        if results_form.is_valid():
            result = results_form.save(commit=False)
            result.competition = competition
            result.save()
            return redirect(
                "dashboard:competition_detail", competition_id=competition_id
            )
    else:
        results_form = ResultForm()

    results = Result.objects.filter(competition=competition).order_by("event", "round")
    return render(
        request,
        "dashboard/competition_detail.html",
        {"competition": competition, "form": results_form, "results": results},
    )


@login_required
def delete_competition_view(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    if request.method == "POST":
        competition.delete()

    return redirect("dashboard:dashboard")


@login_required
def edit_result_view(request, competition_id, result_id):
    competition = get_object_or_404(Competition, id=competition_id)
    result = get_object_or_404(Result, id=result_id, competition=competition)

    if request.method == "POST":
        form = ResultForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            return redirect(
                "dashboard:competition_detail", competition_id=competition.id
            )
    else:
        form = ResultForm(instance=result)

    return render(
        request,
        "dashboard/edit_result.html",
        {"form": form, "competition": competition, "result": result},
    )


@login_required
def delete_result_view(request, competition_id, result_id):
    competition = get_object_or_404(Competition, id=competition_id)
    result = get_object_or_404(Result, id=result_id, competition=competition)

    if request.method == "POST":
        result.delete()

    return redirect("dashboard:competition_detail", competition_id=competition.id)
