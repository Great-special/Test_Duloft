from django.shortcuts import render, redirect, reverse
from django.db.models import Q
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.mixins import  LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

# Create your views here.

from cities_light.models import Country, Region, SubRegion

from .models import HouseModel, FlatModel, SpaceModel
from .forms import FlatModelForm, HouseModelForm, SpaceModelForm, LookUpForm, location_searchform



def index_view(request):
    properties = HouseModel.objects.all()
    lastest_pro = properties.order_by('-added')[0:6]
    featured = properties.filter(featured=True)
    form = LookUpForm()
    
    if request.method == 'POST':
        form = LookUpForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data.get('location')
            Btype = form.cleaned_data.get('building_type')
            Atype = form.cleaned_data['accommodation_type']
            min_price = form.cleaned_data['min_price']
            max_price = form.cleaned_data['max_price']
            
            queryset = FlatModel.objects.filter(Q(house__state__name__icontains = location) | Q(house__city__name__icontains = location)
                                                | Q(house__address__icontains = location)).filter(house__building_type = Btype, accommodation_type = Atype)
            print(queryset)
            if not queryset:
                queryset = SpaceModel.objects.filter(Q(house__state__name__icontains = location) | Q(house__city__name__icontains = location)
                                                | Q(house__address__icontains = location)).filter(house__building_type = Btype, accommodation_type = Atype)
                print(queryset, 'if')
                
            if max_price >= min_price:
                finalset = queryset.filter(Q(price__range = (min_price, max_price)) 
                                       | Q(house__house_price__range = (min_price, max_price)))
                print(finalset, 'finalset')
                return render(request, 'search_results.html', {'results':finalset})
                
            else:
                finalset = queryset.filter(Q(price__range = (max_price, min_price)) 
                                       | Q(house__house_price__range = (max_price, min_price)))
                return render(request, 'search_results.html', {'results':finalset})
            
    return render(request, 'homepage.html', {'form':form, 'properties':featured, "lastest_pro":lastest_pro})

class HouseModelListView(ListView): #LoginRequiredMixin
    template_name = 'houses.html'
    context_object_name = "houses"
    queryset = HouseModel.objects.all()
      
# def houses_list(request):
#     houses = HouseModel.objects.all()
#     context = {
#         'houses': houses,
#     }
#     return render(request, 'houses.html', context)


class HouseModelDetailView(DetailView): #LoginRequiredMixin
    template_name = 'house_details.html'
    context_object_name = "house"
    queryset = HouseModel.objects.all()
    
# def lead_detail(request, id):
#     lead = Lead.objects.get(id=id)
#     context = {
#         'lead': lead,
#     }
#     return render(request, 'leads/lead_details.html', context)

class FlatModelDetailView(DetailView): #LoginRequiredMixin
    template_name = 'flat_details.html'
    context_object_name = "flat"
    queryset = FlatModel.objects.all()


class SpaceModelDetailView(DetailView): #LoginRequiredMixin
    template_name = 'space_details.html'
    context_object_name = "space"
    queryset = SpaceModel.objects.all()
    

def house_create_view(request):
    template_name = 'page-add-new-property.html'
    
    if request.method == "POST":
        # Setting the house landlord to the loggedin user
        form = HouseModelForm(request.POST, request.FILES)
        if form.is_valid():
            house_instance = form.save(commit = False)
            if request.user.is_landlord:
                house_instance.landlord = request.user
                house_instance.save()
                return redirect('my-properties-dashboard')
            else:
                return HttpResponseBadRequest("You cannot add a house")
    else:
        form = HouseModelForm()

    return render(request, template_name, {'form':form})



def flat_create_view(request):
    template_name = 'add_flat.html'
    print(request.user, 'BE')
    if request.method == "POST":
        # Setting the house landlord to the loggedin user
        print(request.user, 'AF')
        form = FlatModelForm(request.user, request.POST, request.FILES,)
        if form.is_valid():
            flat_instance = form.save(commit = False)
            if request.user.is_landlord:
                if flat_instance.house.landlord == request.user:
                    flat_instance.save()
                    return redirect('my-apartment-dashboard')
                else:
                    return HttpResponseBadRequest("You cannot add a flat to this house")
            else:
                return HttpResponseBadRequest("You cannot add a flat")
    else:
        form = FlatModelForm(request.user)

    return render(request, template_name, {'form':form})


def space_create_view(request):
    template_name = 'add_flat.html'
    
    if request.method == "POST":
        # Setting the house landlord to the loggedin user
        form = SpaceModelForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            space_instance = form.save(commit = False)
            if request.user.is_landlord:
                if space_instance.house.landlord == request.user:
                    space_instance.save()
                    return redirect('my-space-dashboard')
                else:
                    return HttpResponseBadRequest("You cannot add a space to this house")
            else:
                return HttpResponseBadRequest("You cannot add a space")
    else:
        form = SpaceModelForm(request.user)

    return render(request, template_name, {'form':form})


def house_update_view(request, id):
    
    house = HouseModel.objects.get(id = id)
    form = HouseModelForm(instance = house)
    
    if request.method == 'POST':
        form = HouseModelForm(request.POST, request.FILES, instance = house)
        if form.is_valid():
            form.save()
            return redirect('/')
        
    context = {
        'house': house, 
        'form': form, 
    }
    template_name = 'page-add-new-property.html'
    return render( request, template_name, context)


def flat_update_view(request, id):
    flat = FlatModel.objects.get(id = id)
    form = FlatModelForm(instance = flat)
    
    if request.method == 'POST':
        form = FlatModelForm(request.POST, request.FILES, instance = flat)
        if form.is_valid():
            form.save()
            return redirect('/')
        
    context = {
        'flat': flat, 
        'form': form, 
    }
    template_name = 'update_flat.html'
    return render( request, template_name, context)


def space_update_view(request, id):
    flat = SpaceModel.objects.get(id = id)
    form = SpaceModelForm(instance = flat)
    
    if request.method == 'POST':
        form = SpaceModelForm(request.POST, request.FILES, instance = flat)
        if form.is_valid():
            form.save()
            return redirect('/')
        
    context = {
        'flat': flat, 
        'form': form, 
    }
    template_name = 'update_flat.html'
    return render( request, template_name, context)


def get_flats_by_building(request, pk):
    try:
        flats = FlatModel.objects.filter(house = pk)
        spaces = SpaceModel.objects.filter(house = pk)
    except:
        pass
    
    house_id = pk
    context = {
        'flats':flats, 
        'spaces':spaces,
        'house_id':house_id
    }
    print(flats)
    return render(request, 'flatsPerhouse.html', context)



def lookup_accommodation(request, keyword: str):
    # returns the objects where the house.state OR house.city contains the search word
    # if 'Mall' in keyword or 'shop' in keyword:
    #     print('in if ->')
    #     other_queryset = SpaceModel.objects.filter(Q(house__state__name__icontains=keyword) 
    #                     | Q(accommodation_type__icontains=keyword) | Q(house__address__icontains=keyword) | Q(house__city__name__icontains=keyword))
    #     print(others_queryset)
    #     return render(request, 'search_results.html', {'other-results': other_queryset})
    # else:
    #     print('in else ->')
    #     queryset = FlatModel.objects.filter(Q(house__state__name__icontains=keyword) 
    #                         | Q(accommodation_type__icontains=keyword) |Q(house__address__icontains=keyword) | Q(house__city__name__icontains=keyword))
    #     print(queryset)
    #     return render(request, 'search_results.html', {'apartment_results': queryset})
    
    queryset = FlatModel.objects.filter(Q(house__state__name__icontains=keyword) 
                        | Q(accommodation_type__icontains=keyword) | Q(house__address__icontains=keyword) | Q(house__city__name__icontains=keyword))
    if not queryset:
        queryset = SpaceModel.objects.filter(Q(house__state__name__icontains=keyword) 
                        | Q(accommodation_type__icontains=keyword) | Q(house__address__icontains=keyword) | Q(house__city__name__icontains=keyword))
        print(queryset, 'if')
    print(queryset, 'out')    
    return render(request, 'search_results.html', {'results': queryset})

def lookup_property_by_type(request, keyword: str):
    # returns the objects where the house.state OR house.city contains the search word
    queryset = HouseModel.objects.filter(building_type__icontains=keyword)
    print(queryset)
    return render(request, 'property_search_results.html', {'results':queryset})  

# def lookup_prices(request):
#     # returns the objects where the prices of the flats are greater than or equal to the search price
#     # Or where the prices of the House are greater than or equal to the search price
#     queryset = FlatModel.objects.filter(Q(price__gte=20000) | Q(house_house_price__gte=20000))
    
#     # returns the objects where the prices are between the search prices
#     # Or where the house prices are between the search prices
#     queryset = FlatModel.objects.filter(Q(price__range=(20000, 30000)) | Q(house_house_price__range=(20000, 30000)))
    
#     return render(request, 'search_results.html', {'results':queryset})


def lookupform_view(request):
    form = LookUpForm()
    
    if request.method == 'POST':
        form = LookUpForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data.get('location')
            Btype = form.cleaned_data.get('building_type')
            Atype = form.cleaned_data['accommodation_type']
            min_price = form.cleaned_data['min_price']
            max_price = form.cleaned_data['max_price']
            
            queryset = FlatModel.objects.filter(Q(house__state__name__icontains = location) |Q(house__city__name__icontains = location)
                                                | Q(house__address__icontains = location)).filter(house__building_type = Btype, accommodation_type = Atype)
            print(queryset)
            if max_price >= min_price:
                finalset = queryset.filter(Q(price__range = (min_price, max_price)) 
                                       | Q(house__house_price__range = (min_price, max_price)))
                print(finalset)
                return render(request, 'search_results.html', {'results':finalset})
                
            else:
                finalset = queryset.filter(Q(price__range = (max_price, min_price)) 
                                       | Q(house__house_price__range = (max_price, min_price)))
                return render(request, 'search_results.html', {'results':finalset})
            
    return render(request, 'search_form.html', {'form':form})
     
     


# Ajax Functions      
def load_states(request):
    country_id = request.GET.get('country')
    states = Region.objects.filter(country_id = country_id).order_by('name')
    # cities = City.objects.filter
    print(country_id)
    return render(request, 'options_value.html', {'datas': states})
    # return JsonResponse(list(states.values('id', 'name')), safe = False)

def load_cities(request):
    state_id = request.GET.get('state')
    cities = SubRegion.objects.filter(region_id = state_id).order_by('name')
    print(state_id)
    return render(request, 'options_value.html', {'datas': cities})

