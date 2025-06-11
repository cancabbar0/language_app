import json
import random
from datetime import datetime, timedelta, timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from language_app.forms import WordsForm
from .models import UserWords, Words, QuestionCount


@login_required(login_url=reverse_lazy("login"))
def home_view(request):
    return render(request, "home.html")


@login_required(login_url=reverse_lazy("login"))
def quiz_view(request):
    user = request.user
    if request.method == "POST":
        correct_answers = []
        wrong_answers = []
        data = json.loads(request.body)
        answer_datas = data.get('answer_data', [])
        for answer_data in answer_datas:
            word = Words.objects.get(english=answer_data.get('question'))
            if answer_data.get('answer') == word.turkish:
                correct_answers.append(UserWords.objects.get(user_id=user.id, word_id=word.id))
            else:
                wrong_answers.append(UserWords.objects.get(user_id=user.id, word_id=word.id))

        for correct_answer in correct_answers:
            correct_answer.corect_count += 1
            if correct_answer.corect_count == 7:
                correct_answer.is_learned = True
            correct_answer.save()

        for wrong_answer in wrong_answers:
            wrong_answer.corect_count = 0
            wrong_answer.save()

        return HttpResponse(json.dumps({"correct": len(correct_answers), "wrong": len(wrong_answers)}),
                            content_type="application/json")

    else:
        now = datetime.now(timezone.utc)
        one_day_ago = now - timedelta(days=1)
        one_week_ago = now - timedelta(days=7)
        one_month_ago = now - timedelta(days=30)
        three_month_ago = now - timedelta(days=90)  # Fixed typo from tree_month_ago
        six_month_ago = now - timedelta(days=180)
        one_year_ago = now - timedelta(days=365)

        words = []
        word_count = 0
        question_count = QuestionCount.objects.get(id=user.id)
        unique_words = set()  # Using a set to keep track of unique words

        userwords = []
        all_userwords = UserWords.objects.filter(user_id=user.id, is_learned=0)  # Fetch all words from the database
        for all_userword in all_userwords:
            if all_userword.corect_count == 0:
                userwords.append(Words.objects.get(id=all_userword.word_id))
            if all_userword.corect_count == 1 and all_userword.updated_date < one_day_ago:
                userwords.append(Words.objects.get(id=all_userword.word_id))
            if all_userword.corect_count == 2 and all_userword.updated_date < one_week_ago:
                userwords.append(Words.objects.get(id=all_userword.word_id))
            if all_userword.corect_count == 3 and all_userword.updated_date < one_month_ago:
                userwords.append(Words.objects.get(id=all_userword.word_id))
            if all_userword.corect_count == 4 and all_userword.updated_date < three_month_ago:
                userwords.append(Words.objects.get(id=all_userword.word_id))
            if all_userword.corect_count == 5 and all_userword.updated_date < six_month_ago:
                userwords.append(Words.objects.get(id=all_userword.word_id))
            if all_userword.corect_count == 6 and all_userword.updated_date < one_year_ago:
                userwords.append(Words.objects.get(id=all_userword.word_id))

        while word_count < question_count.ask_count and len(unique_words) < len(userwords):
            random_word = random.choice(userwords)
            if random_word.english not in unique_words:
                word_count += 1
                unique_words.add(random_word.english)
                choises = [random_word.turkish]
                # Ensure choices are unique and do not duplicate the correct answer
                selected_choises = random.sample([w for w in userwords if w.id != random_word.id], 4)
                for selected_choise in selected_choises:
                    choises.append(selected_choise.turkish)

                random.shuffle(choises)
                question_data = {
                    'question': random_word.english,
                    'img': random_word.img.url if random_word.img else None,  # Include image if available
                    'choices0': choises[0],
                    'choices1': choises[1],
                    'choices2': choises[2],
                    'choices3': choises[3],
                    'choices4': choises[4],
                }
                words.append(question_data)

        return render(request, "quiz.html", {"words": words})


@login_required(login_url=reverse_lazy("login"))
def add_word_view(request):
    if request.method == 'POST':
        user = request.user
        response_data = {}
        try:
            form = WordsForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()

                # Add the word to the userwords table
                word = Words.objects.get(english=form.cleaned_data.get("english"))
                userwords = UserWords.objects.create(user_id=user.id, word_id=word.id)
                userwords.save()

                response_data["error"] = False
                response_data["result"] = "Word added successfully"
            else:
                response_data["error"] = True
                response_data["result"] = "Form is not valid"
        except Exception as e:
            response_data["error"] = True
            response_data["result"] = str(e)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        form = WordsForm()
    return render(request, 'add_word.html', {'form': form})


@login_required(login_url=reverse_lazy("login"))
def settings_view(request):
    user = request.user
    if request.method == "POST":
        response_data = {}
        if request.POST.get("status") == "change_ask_count":
            try:
                question_count = QuestionCount.objects.get(id=user.id)
                question_count.ask_count = request.POST.get("ask_count")
                question_count.save()
                response_data["error"] = False
                response_data["result"] = "Ask count changed successfully"
            except Exception as e:
                response_data["error"] = True
                response_data["result"] = str(e)
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        question_count = QuestionCount.objects.get(id=user.id)
        return render(request, "settings.html", {"ask_count": question_count.ask_count})


@login_required(login_url=reverse_lazy("login"))
def get_analize_report(request):
    user = request.user
    userwords = UserWords.objects.filter(user_id=user.id)
    analise_datas = []
    total_percent = []
    for userword in userwords:
        analise_data = {}
        word = Words.objects.get(id=userword.word_id)
        analise_data["english"] = word.english
        analise_data["turkish"] = word.turkish
        analise_data["in_sentence"] = word.in_sentence
        analise_data["corect_count"] = userword.corect_count
        analise_data["is_learned"] = userword.is_learned

        percent = (userword.corect_count / 7) * 100
        total_percent.append(percent)
        analise_data["percent"] = float("{:.2f}".format(percent))

        analise_datas.append(analise_data)
    total_percent = sum(total_percent) / len(total_percent)
    analise_datas.append({"total_percent": total_percent})
    return render(request, "analize_report.html", {"analise_datas": analise_datas})