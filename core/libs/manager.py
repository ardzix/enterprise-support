'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: manager.py
# Project: core.wecare.id
# File Created: Monday, 17th December 2018 10:59:03 pm
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Monday, 17th December 2018 10:59:04 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Handcrafted and Made with Love
# Copyright - 2018 Wecare.Id, wecare.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from taggit.managers import TaggableManager, _TaggableManager
from django.utils import six
from django.conf import settings
from django.db import models, router
from django.db.models import signals, F
from taggit.utils import (require_instance_manager)
from core.structures.tag.models import TagGroup


class _TagManager(_TaggableManager):
    @require_instance_manager
    def incr(self, *tags, **kwargs):
        factor = kwargs.get("factor", 1)
        db = router.db_for_write(self.through, instance=self.instance)
        tag_objs = self._to_tag_model_instances(tags)

        for tag in tag_objs:
            obj, created = self.through._default_manager.using(db).get_or_create(
                tag=tag, **self._lookup_kwargs())

            if created:
                obj.weight = 1
            else:
                obj.weight = obj.weight + factor

            obj.save()

    @require_instance_manager
    def decr(self, *tags, **kwargs):
        factor = kwargs.get("factor", 1)
        db = router.db_for_write(self.through, instance=self.instance)
        tag_objs = self._to_tag_model_instances(tags)

        for tag in tag_objs:
            obj, created = self.through._default_manager.using(db).get_or_create(
                tag=tag, **self._lookup_kwargs())

            if created:
                obj.weight = 1
            elif (obj.weight - factor) >= factor:  # can not less than 1
                obj.weight = obj.weight - factor
            else:
                obj.weight = 1

            obj.save()

    @require_instance_manager
    def add(self, *tags):
        db = router.db_for_write(self.through, instance=self.instance)

        tag_objs = self._to_tag_model_instances(tags)
        new_ids = set(t.pk for t in tag_objs)

        # NOTE: can we hardcode 'tag_id' here or should the column name be got
        # dynamically from somewhere?
        vals = (self.through._default_manager.using(db)
                .values_list('tag_id', flat=True)
                .filter(**self._lookup_kwargs()))

        new_ids = new_ids - set(vals)

        signals.m2m_changed.send(
            sender=self.through, action="pre_add",
            instance=self.instance, reverse=False,
            model=self.through.tag_model(), pk_set=new_ids, using=db,
        )

        for tag in tag_objs:
            self.through._default_manager.using(db).get_or_create(
                tag=tag, **self._lookup_kwargs())

        signals.m2m_changed.send(
            sender=self.through, action="post_add",
            instance=self.instance, reverse=False,
            model=self.through.tag_model(), pk_set=new_ids, using=db,
        )

    @require_instance_manager
    def remove(self, *tags):
        if not tags:
            return

        db = router.db_for_write(self.through, instance=self.instance)

        qs = (self.through._default_manager.using(db)
              .filter(**self._lookup_kwargs())
              .filter(tag__name__in=tags))

        old_ids = set(qs.values_list('tag_id', flat=True))

        signals.m2m_changed.send(
            sender=self.through, action="pre_remove",
            instance=self.instance, reverse=False,
            model=self.through.tag_model(), pk_set=old_ids, using=db,
        )
        qs.delete()
        signals.m2m_changed.send(
            sender=self.through, action="post_remove",
            instance=self.instance, reverse=False,
            model=self.through.tag_model(), pk_set=old_ids, using=db,
        )

    def _to_tag_model_instances(self, tags):
        """
        Takes an iterable containing either strings, tag objects, or a mixture
        of both and returns set of tag objects.
        """
        db = router.db_for_write(self.through, instance=self.instance)

        str_tags = set()
        tag_objs = set()

        for t in tags:
            if isinstance(t, self.through.tag_model()):  # is object
                tag_objs.add(t)
            elif isinstance(t, six.string_types):  # is string
                str_tags.add(t)
            else:
                raise ValueError(
                    "Cannot add {0} ({1}). Expected {2} or str.".format(
                        t, type(t), type(self.through.tag_model())))

        tag_delimiter = getattr(settings, 'TAGGIT_TAG_DELIMITER', ':')
        case_insensitive = getattr(settings, 'TAGGIT_CASE_INSENSITIVE', True)
        manager = self.through.tag_model()._default_manager.using(db)

        existing = []
        tags_to_create = []

        if case_insensitive:
            # Some databases can do case-insensitive comparison with IN, which
            # would be faster, but we can't rely on it or easily detect it.
            for raw_name in str_tags:
                try:
                    group, name = raw_name.split(tag_delimiter)
                    tag = manager.get(
                        group__short_name__iexact=group,
                        name__iexact=name
                    )
                    existing.append(tag)
                except self.through.tag_model().DoesNotExist:
                    tags_to_create.append(raw_name)
        else:
            # If str_tags has 0 elements Django actually optimizes that to not
            # do a query.  Malcolm is very smart.
            for raw_name in str_tags:
                try:
                    group, name = raw_name.split(tag_delimiter)
                    tag = manager.filter(
                        group__short_name__exact=group,
                        name__exact=name
                    )
                    existing.append(tag)
                except self.through.tag_model().DoesNotExist:
                    tags_to_create.append(raw_name)

        tag_objs.update(existing)

        for new_record in tags_to_create:
            new_group, new_tag = new_record.split(tag_delimiter)

            # check new group is existing or not
            groups = TagGroup.objects.filter(
                short_name=new_group
            )

            # ignore if not exist
            if groups.exists() is False:
                return

            # get the first record if group is exist
            group = groups.first()

            if case_insensitive:
                try:
                    tag = manager.get(
                        group__short_name__iexact=new_group,
                        name__iexact=new_tag
                    )
                except self.through.tag_model().DoesNotExist:
                    tag = manager.create(
                        group=group,
                        name=new_tag
                    )
            else:
                tag = manager.create(
                    group=group,
                    name=new_tag
                )

            tag_objs.add(tag)

        return tag_objs


class TagManager(TaggableManager):
    def __init__(self, *args, **kwargs):
        kwargs["manager"] = _TagManager
        super(TagManager, self).__init__(*args, **kwargs)
