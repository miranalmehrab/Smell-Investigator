mark_safe('<python code here>')

r = mark_safe('<python code here>')

img = format_html('<a target="_blank" href="{}">{}</a>',
        obj.manifest.extra_data['rendering']['@id'],
        mark_safe(img))

arg_vals.append(mark_safe(arg))
raise forms.ValidationError(mark_safe(msg))
return [mark_safe(obj) for obj in value]

f.title = mark_safe(f.title)
yield mark_safe(form[cl.model._meta.pk.name])
messages.success(self.request, mark_safe(message))
context['related_url'] = mark_safe(related_url)

def my_func():
    return mark_safe('<function return code>')

    # return render_to_string(
    #     WIDGET_TEMPLATE,
    #     {'api_server': server,
    #      'public_key': public_key,
    #      'error_param': error_param,
    #      'lang': lang,
    #      'options': mark_safe(json.dumps(attrs, indent=2))
    #      })

    # return mark_safe(renderer.render('ckeditor/widget.html', {
    #         'final_attrs': flatatt(final_attrs),
    #         'value': conditional_escape(force_text(value)),
    #         'id': final_attrs['id'],
    #         'config': json_encode(self.config),
    #         'external_plugin_resources': json_encode(external_plugin_resources)
    #     }))
