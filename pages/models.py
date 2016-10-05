from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock


class SimplePage(Page):
    intro = models.CharField(max_length=255,
        help_text='Introductory text below header')

    body = StreamField([
        ('callout', blocks.RichTextBlock(
            help_text='Block to draw users\' attention, e.g. for "See your GP"',
            label='Callout block')),
        ('paragraph', blocks.RichTextBlock(label='Text')),
        ('image', ImageChooserBlock()),

        ('section', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('subsections', blocks.ListBlock(
                blocks.StructBlock([
                    ('title', blocks.CharBlock()),
                    ('content', blocks.StreamBlock([
                        ('image', ImageChooserBlock()),
                        ('text', blocks.RichTextBlock(label='Text')),
                        # ('embed', EmbedBlock()),
                    ]))
                ])
            ))
        ], label='Page section'))
    ])

    aside = StreamField([
        ('alert', blocks.RichTextBlock()),
        ('paragraph', blocks.RichTextBlock()),
    ], help_text="Sidebar content, intended for 'call 999 if...' alerts")

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        StreamFieldPanel('body'),
        StreamFieldPanel('aside')
    ]

    api_fields = ['title', 'intro', 'body', 'aside']
