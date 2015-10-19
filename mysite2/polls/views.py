from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect #, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Ma_Part, Mn_Name
from .models import Choice

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
#q = Question.objects.filter( pub_date__lte=timezone.now() ).order_by('-pub_date')
          
        q = Question.objects.filter( pub_date__lte=timezone.now(),
            choice__isnull=False
            ).distinct()
        q = q.order_by('-pub_date')
        
        
        #q = Question.objects.raw("select * from polls_question")
        
        """for c in q:
            if len(c.choice_set.all()) == 0:
                #print(q, "XXXXXXX")
                q = q.exclude(id=c.id)
        """
        
            
        return q[:5]
    
        
        
class DetailView(generic.DetailView):
    model = Question
    #template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
        

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
         

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
        
#class Ma_PartView(generic.ListView):
    #


from django.http import HttpResponse


def listParts():
    parts = Ma_Part.objects.order_by('ma_desc')

    output = ''
    for p in parts:
        #print p.mn_id

        output += '<p>{0}: {1}  - {2}: {3}</p>'.format(str(p.ma_id), p.ma_desc, p.mn_id.mn_name, p.mn_nr)
    return output

def indexHello(request):
    parts = Ma_Part.objects.order_by('ma_desc')

    output = ''
    for p in parts:
        #print p.mn_id

        output += '<p>{0}: {1}  - {2}: {3}</p>'.format(str(p.ma_id), p.ma_desc, p.mn_id.mn_name, p.mn_nr)


    ax, c = Mn_Name.objects.get_or_create(mn_name='Axicon')
    axp = Ma_Part.objects.create(ma_id=102, ma_desc='Ax 2', mn_id=ax, mn_nr='1010101', mn_desc='foo ooo o o')
    axp.save()


    output += listParts()


    return HttpResponse( output )

