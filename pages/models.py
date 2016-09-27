from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock


class SimplePage(Page):
    # title = models.CharField(max_length=255)
    intro = models.CharField(max_length=255)
    date = models.DateField("Post date")

    body = StreamField([
        ('callout', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('paragraph', blocks.RichTextBlock()),
        ])),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),

        ('section', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('subsections', blocks.ListBlock(
                blocks.StructBlock([
                    ('title', blocks.CharBlock()),
                    ('image', ImageChooserBlock()),
                    ('body', blocks.RichTextBlock())
                ])
            ))
        ])),

        # ('section', blocks.ListBlock(
        #     blocks.StructBlock([
        #         ('title', blocks.CharBlock()),
        #         ('image', ImageChooserBlock()),
        #         ('body', blocks.RichTextBlock())
        #     ], label="Subsection")
        # ))
    ])

    aside = StreamField([
        ('alert', blocks.RichTextBlock()),
        ('paragraph', blocks.RichTextBlock()),
    ])

    content_panels = Page.content_panels + [
        # FieldPanel('title'),
        FieldPanel('intro'),
        FieldPanel('date'),
        StreamFieldPanel('body'),
        StreamFieldPanel('aside')
    ]

    api_fields = ['title', 'intro', 'date', 'body', 'aside']
