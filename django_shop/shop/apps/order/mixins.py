from django.http.response import HttpResponse
from django.template.loader import render_to_string


import csv
from weasyprint import HTML

class BaseExport:
    content_type_export = None

    def get_response_obj(self, name):
        response = HttpResponse(content_type=self.content_type_export)
        response['Content-Disposition'] = 'filename="%s"' % name
        return response

class ExportToCSVMixin(BaseExport):
    csv_filename = 'default.csv'
    content_type_export = 'text/csv'

    def get_row(self, queryset):
        model = queryset.model
        fields = [f for f in model._meta.get_fields() if not f.many_to_many]
        response = self.get_response_obj(self.csv_filename)
        yield fields, response
        for obj in queryset:
            row = [getattr(obj, f.name) if hasattr(obj, f.name)
                    else list(getattr(obj, f.name+'_set').values('id')) for f in fields]
            yield row

    def to_csv(self, req, queryset):
        start_row = self.get_row(queryset)
        fields, response = next(start_row)
        writer = csv.writer(response)
        writer.writerow((f.verbose_name if hasattr(f, 'verbose_name') else f.name + ' id' for f in fields))
        for row in start_row:
            writer.writerow(row)
        return response


class ExportToPDFMixin(BaseExport):
    pdf_template = None
    pdf_filename = 'default.pdf'
    content_type_export = 'application/pdf'

    def to_pdf(self, context):
        response = self.get_response_obj(self.pdf_filename)
        html = render_to_string(self.pdf_template, context)
        HTML(string=html).write_pdf(response)
        return response


