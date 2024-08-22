from .common import *

def extract_questions_from_docx(docx_file):
    try:
        doc = Document(docx_file)
        questions = []

        for table in doc.tables:
            question_data = {
                "question": "",
                "options": [],
                "answer": ""
            }
            options = []
            question_found = False

            for row in table.rows:
                cells = row.cells
                if len(cells) < 2:
                    continue

                header = cells[0].text.strip()
                value = cells[1].text.strip()

                if header == 'Question':
                    question_data["question"] = value
                    question_found = True
                elif header in ['A', 'B', 'C', 'D']:
                    options.append(value)
                elif header == 'Answer':
                    question_data["answer"] = value

            if question_found:
                question_data["options"] = options[:4]  # Ensure we only have 4 options
                questions.append(question_data)

        return questions

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Create your views here.    
@login_required
def exam_creation(request):
    if request.method == 'POST':
        form = ExamForm(request.POST, request.FILES)
        if form.is_valid():
            exam = form.save()  # Save the exam instance

            # Process the Word file
            docx_file = request.FILES.get('docx_file')
            if docx_file:
                questions = extract_questions_from_docx(docx_file)

                if not questions:
                    messages.error(request, 'No questions found in the Word file.')
                    return redirect('dashboard')

                # Save questions to the database
                for q in questions:
                    Question.objects.create(
                        exam=exam,
                        question_text=q["question"],
                        option1=q["options"][0] if len(q["options"]) > 0 else '',
                        option2=q["options"][1] if len(q["options"]) > 1 else '',
                        option3=q["options"][2] if len(q["options"]) > 2 else '',
                        option4=q["options"][3] if len(q["options"]) > 3 else '',
                        correct_option=q["answer"]
                    )

                messages.success(request, 'Exam created and questions imported successfully.')
                return redirect('dashboard')
    else:
        form = ExamForm()

    return render(request, 'exam_creation.html', {'form': form})


@login_required
def edit_question(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = Question.objects.filter(exam=exam)
    context = {
        'exam': exam,
        'questions': questions,
    }
    return render(request, 'edit_questions.html', context)

# Save (edit or add) questions
@require_POST
def save_all_questions(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    data = json.loads(request.body)

    for question_data in data:
        question_id = question_data.get('id')
        question_text = question_data.get('question_text')
        option1 = question_data.get('option1')
        option2 = question_data.get('option2')
        option3 = question_data.get('option3')
        option4 = question_data.get('option4')
        correct_answer = question_data.get('correct_option')
        
        if question_id:  # Existing question, update it
            question = get_object_or_404(Question, id=question_id, exam=exam)
            question.question_text = question_text
            question.option1 = option1
            question.option2 = option2
            question.option3 = option3
            question.option4 = option4
            question.correct_option = correct_answer
            question.save()
        else:  # New question, create it
            Question.objects.create(
                exam=exam,
                question_text=question_text,
                option1=option1,
                option2=option2,
                option3=option3,
                option4=option4,
                correct_option=correct_answer
            )
    
    return JsonResponse({'status': 'success'})


@require_http_methods(["DELETE"])
def delete_question(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        question.delete()
        return JsonResponse({'success': True})
    except Question.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Question does not exist'})


@require_http_methods(["DELETE"])
def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    exam.delete()
    return JsonResponse({'success': True})



@login_required
def edit_exam(request, j):
    exam = get_object_or_404(Exam, id=j)

    if request.method == 'POST':
        exam_form = ExamForm(request.POST, instance=exam)

        if exam_form.is_valid():
            exam_form.save()
            return redirect('dashboard')  # Redirect to the exams list or another appropriate page

    else:
        exam_form = ExamForm(instance=exam)

    context = {
        'exam_form': exam_form,
        'exam': exam,
    }
    return render(request, 'edit_exam.html', context)

