from django.contrib import admin

from .models import Message, ChatRoom

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'message', 'timestamp', ]
    list_filter = ('sender', )
    ordering = ('-timestamp', 'sender',)
    search_fields = ('sender','message',)

admin.site.register(ChatRoom)
