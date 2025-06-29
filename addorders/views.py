from django.shortcuts import render, redirect
from .models import Order
from django.utils import timezone
from openpyxl import Workbook
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from io import BytesIO

SHOP_CODES = [
    1022, 1026, 1029, 1030, 1031, 1033, 1034, 1036, 1038, 1039,
    1040, 1042, 1045, 1046, 1047, 1048, 1050, 1051, 1052, 1053,
    1054, 1055, 1056, 1057, 1058, 1061, 1062, 1063, 1065, 1069,
    1070, 1071, 1074, 1075, 1076, 1077, 1078, 1084, 1087, 1088,
    1093, 1096, 1097, 1098, 1099, 1102, 1103, 1104, 1105, 1106,
    1107, 1108, 1111, 1115, 1117, 1119, 1120, 1121, 1131, 1134,
    5001, 5002, 7012, 7013, 7014, 7015, 7016, 7017, 7018, 7019,
    7020, 7021, 7022, 7023, 7024, 7025, 7026, 7027, 7028, 7029,
    7030, 7031, 7032, 7033, 7035, 7036, 7037, 7043, 7046
]

def add_order(request):
    if 'order_data' not in request.session:
        request.session['order_data'] = []
        request.session['current_index'] = 0
        request.session['finished'] = False

    order_data = request.session['order_data']
    index = request.session['current_index']
    finished = request.session.get('finished', False)

    if request.method == 'POST':
        if 'cancel' in request.POST:
            request.session.flush()
            return redirect('add_order')

        if 'confirm' in request.POST:
            article = request.session['article']
            product_name = request.session['product_name']

            filtered_order_data = [row for row in order_data if row[1] > 0]

            wb = Workbook()
            ws = wb.active
            ws.title = "Замовлення"
            ws.append(["Магазин", "Кількість"])
            for row in filtered_order_data:
                ws.append(row)

            excel_file = BytesIO()
            wb.save(excel_file)
            excel_file.seek(0)

            filename = f"{article}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            path = default_storage.save(f"order_excels/{filename}", ContentFile(excel_file.read()))

            Order.objects.create(
                article=article,
                product_name=product_name,
                file=path
            )

            request.session.flush()
            return redirect('add_order')

        elif 'edit' in request.POST:
            edit_index = int(request.POST.get('edit_index'))
            new_value = int(request.POST.get('new_value'))
            order_data[edit_index] = (order_data[edit_index][0], new_value)
            request.session['order_data'] = order_data

        elif 'finish_list' in request.POST:
            for i in range(index, len(SHOP_CODES)):
                order_data.append((SHOP_CODES[i], 0))
            request.session['order_data'] = order_data
            request.session['current_index'] = len(SHOP_CODES) + 1
            request.session['finished'] = True
            return redirect('add_order')

        elif index == 0:
            article = request.POST.get('article')
            name = request.POST.get('product_name')
            request.session['article'] = article
            request.session['product_name'] = name
            request.session['current_index'] = 1
            return redirect('add_order')

        elif index <= len(SHOP_CODES):
            box_count = int(request.POST.get('box_count'))
            shop_code = SHOP_CODES[index - 1]
            order_data.append((shop_code, box_count))
            request.session['order_data'] = order_data
            request.session['current_index'] = index + 1

    current_index = request.session.get('current_index', 1)
    context = {
        'session_ready': current_index > 0,
        'current_index': current_index,
        'total_shops': len(SHOP_CODES),
        'current_shop': SHOP_CODES[current_index - 1] if current_index <= len(SHOP_CODES) else '',
        'order_table': request.session.get('order_data', []),
        'all_entered': current_index > len(SHOP_CODES),
        'finished': request.session.get('finished', False),
    }

    return render(request, 'add_orders/index.html', context)