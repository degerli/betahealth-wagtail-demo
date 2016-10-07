from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

from exporter.models import BakeryModel


class SimplePage(Page, BakeryModel):
    intro = models.CharField(max_length=255)

    body = StreamField([
        ('callout', blocks.RichTextBlock()),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),

        ('section', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('subsections', blocks.ListBlock(
                blocks.StructBlock([
                    ('title', blocks.CharBlock()),
                    ('content', blocks.StreamBlock([
                        ('image', ImageChooserBlock()),
                        ('text', blocks.RichTextBlock()),
                        ('embed', EmbedBlock()),
                    ]))
                ])
            ))
        ]))
    ])

    aside = StreamField([
        ('alert', blocks.RichTextBlock()),
        ('paragraph', blocks.RichTextBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        StreamFieldPanel('body'),
        StreamFieldPanel('aside')
    ]

    api_fields = ['title', 'intro', 'body', 'aside']
    bakery_views = ('pages.bakery_views.SimplePageStatic',)
