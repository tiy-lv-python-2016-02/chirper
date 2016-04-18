import stripe
from chirps.models import Chirp, Pledge
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    chirps = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'chirps')


class ChirpSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Chirp
        fields = '__all__'


class PledgeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    chirp = ChirpSerializer(read_only=True)

    class Meta:
        model = Pledge
        fields = ('id', 'user', 'chirp', 'amount', 'created_at', 'modified_at')


class ChargeSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=50)
    chirp_id = serializers.IntegerField()
    amount = serializers.IntegerField()

    def create(self, validated_data):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        amount = validated_data['amount']
        user = validated_data['user']
        chirp = validated_data['chirp_id']

        charge_id = "ch_IAMNOTAREALNUMBER"
        # try:
        #     charge = stripe.Charge.create(
        #         amount=amount*100,  # amount in cents, again
        #         currency="usd",
        #         source=token,
        #         description="Donation to chirp"
        #     )
        # except stripe.error.CardError as e:
        #     # The card has been declined
        #     pass

        pledge = Pledge.objects.create(user=user,
                                       chirp_id=chirp,
                                       amount=amount,
                                       charge_id=charge_id)

        return pledge




