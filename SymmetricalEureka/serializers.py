# pylint: disable=missing-docstring

from rest_framework import serializers

from .models import SpellListing, SpellClasses


class SpellListingSerializer(serializers.ModelSerializer):
    school = serializers.SerializerMethodField()
    components = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()

    class Meta:
        model = SpellListing
        fields = '__all__'

    # pylint: disable=no-self-use
    def get_school(self, obj):
        return obj.get_school_display()

    def get_components(self, obj):
        return obj.get_components_display()

    def get_level(self, obj):
        return obj.get_level_display()


class SpellClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellClasses
        fields = ('spell', )


class UserSpellSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=256)
    spell = serializers.CharField(max_length=256)

    def update(self, instance, validated_data):
        spell_name = validated_data.get('spell')
        queryset = instance.spells.filter(name=spell_name)
        if queryset.count() == 0:
            spell = SpellListing.get(name=spell_name)
            instance.spells.add(spell)
        else:
            instance.spells.remove(queryset[0])
        instance.save()
        return instance
