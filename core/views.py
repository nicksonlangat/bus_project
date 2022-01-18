import random
from datetime import datetime, timedelta
from core.models import Booking, Bus
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# Create your views here.
@csrf_exempt
def index(request):
    if request.method == 'POST':
        session_id = request.POST.get('sessionId')
        service_code = request.POST.get('serviceCode')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text')

        response = ""

        if text == "":
            response = "CON Welcome! \n Which service would you like to access? \n"  
            response += "1. List all our buses  \n"
            response += "2. Check ticket status \n"
            response += "3. Book a bus seat \n"
            response += "4. Cancel a booking \n"
            response += "5. Report an issue"

        #User needs a list of all buses   
        elif text == "1":
            results=Bus.objects.all()
            for i in results:
                response += f"END {i}:{i.start}-{i.finish} @KSHS{i.price} \n \n"

        elif text == "2":
            response = "CON Choose an option \n"
            response += "1. All tickets \n"
            response += "2. Today active tickets"

         #Follow up
        elif text == '2*1':
            tickets=Booking.objects.filter(
                customer=phone_number
            )
            for tkt in tickets:
                response += f"END Ticket {tkt.id} on {tkt.departure:%Y-%m-%d %H:%M}"

         #Follow up
        elif text == '2*2':
            now = datetime.now()
            tickets=Booking.objects.filter(
                customer=phone_number,
                departure__date=now
            )
            if tickets:
                for tkt in tickets:
                    response += f"END Ticket {tkt.id} on {tkt.departure:%Y-%m-%d %H:%M}"
            response ='END No tickets found'

        #User wants to book a seat
        elif text == "3":
            response = "CON Okay, pick a route \n"
            response += "1. Kericho-Nairobi \n"
            response += "2. Kisumu-Eldoret \n"
            response += "3. Nakuru-Mombasa \n"
            response += "4. Narok-Naivasha "
        
        #Follow up
        elif text == '3*1' or '3*2' or '3*3' or '3*4':
            seat=random.randint(1,30)
            buses=Bus.objects.filter(is_available=True)
            buses=[bus for bus in buses]
            bus=random.choices(buses)
            for i in bus:
                bus=i
            departure=datetime.now() + timedelta(hours=1)
            new_booking=Booking.objects.create(
                bus=bus,
                customer=phone_number,
                seat=seat,
                departure=departure

            )
            response = f"END  Alright! Here is your booking info: \n TICKET NO {new_booking.id} \n Bus Number is {bus} \n Your seat number is {seat} \n Your bus leaves at {departure:%H:%M:%S}"  
        elif text == "4":
            response = "END Feature work in progress, check again soon"
        elif text == "5":
            response = "END Feature work in progress, check again soon"

        return HttpResponse(response)

