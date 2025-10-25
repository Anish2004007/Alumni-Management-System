from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Alumni, Event, Announcement
from .forms import AlumniForm, EventForm, AnnouncementForm
# ---------------- Alumni ----------------
def alumni_list(request):
	q = request.GET.get('q', '').strip()
	alumni = Alumni.objects.all().order_by('-graduation_year', 'name')
	if q:
		# if q is numeric, search graduation_year as well
		if q.isdigit():
			alumni = alumni.filter(Q(name__icontains=q) | Q(graduation_year=int(q)))
		else:
			alumni = alumni.filter(name__icontains=q)
	return render(request, 'alumni/alumni_list.html', {'alumni': alumni, 'q': q})
def alumni_add(request):
	if request.method == 'POST':
		form = AlumniForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('alumni_list')
	else:
		form = AlumniForm()
	return render(request, 'alumni/alumni_form.html', {'form': form, 'title': 'Add Alumni'})
def alumni_edit(request, pk):
	alum = get_object_or_404(Alumni, pk=pk)
	if request.method == 'POST':
		form = AlumniForm(request.POST, instance=alum)
		if form.is_valid():
			form.save()
			return redirect('alumni_list')
	else:
		form = AlumniForm(instance=alum)
	return render(request, 'alumni/alumni_form.html', {'form': form, 'title': 'Edit Alumni'})
def alumni_delete(request, pk):
	alum = get_object_or_404(Alumni, pk=pk)
	if request.method == 'POST':
		alum.delete()
		return redirect('alumni_list')
	return render(request, 'alumni/confirm_delete.html', {'object': alum, 'type': 'Alumni'})
