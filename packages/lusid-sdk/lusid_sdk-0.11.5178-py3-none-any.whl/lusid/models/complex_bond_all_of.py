# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.5178
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid.configuration import Configuration


class ComplexBondAllOf(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'identifiers': 'dict(str, str)',
        'calculation_type': 'str',
        'schedules': 'list[Schedule]',
        'instrument_type': 'str'
    }

    attribute_map = {
        'identifiers': 'identifiers',
        'calculation_type': 'calculationType',
        'schedules': 'schedules',
        'instrument_type': 'instrumentType'
    }

    required_map = {
        'identifiers': 'optional',
        'calculation_type': 'optional',
        'schedules': 'optional',
        'instrument_type': 'required'
    }

    def __init__(self, identifiers=None, calculation_type=None, schedules=None, instrument_type=None, local_vars_configuration=None):  # noqa: E501
        """ComplexBondAllOf - a model defined in OpenAPI"
        
        :param identifiers:  external market codes and identifiers for the bond, e.g. ISIN.
        :type identifiers: dict(str, str)
        :param calculation_type:  The calculation type applied to the bond coupon amount. This is required for bonds that have a particular type of computing the period coupon, such as simple compounding,  irregular coupons etc.  The default CalculationType is `Standard`, which returns a coupon amount equal to Principal * Coupon Rate / Coupon Frequency. Coupon Frequency is 12M / Payment Frequency.  Payment Frequency can be 1M, 3M, 6M, 12M etc. So Coupon Frequency can be 12, 4, 2, 1 respectively.    Supported string (enumeration) values are: [Standard, DayCountCoupon, NoCalculationFloater, BrazilFixedCoupon].
        :type calculation_type: str
        :param schedules:  schedules.
        :type schedules: list[lusid.Schedule]
        :param instrument_type:  The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashFlowsLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap, CashPerpetual, CapFloor, CashSettled, CdsIndex, Basket, FundingLeg, FxSwap, ForwardRateAgreement, SimpleInstrument, Repo, Equity, ExchangeTradedOption, ReferenceInstrument, ComplexBond, InflationLinkedBond, InflationSwap (required)
        :type instrument_type: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._identifiers = None
        self._calculation_type = None
        self._schedules = None
        self._instrument_type = None
        self.discriminator = None

        self.identifiers = identifiers
        self.calculation_type = calculation_type
        self.schedules = schedules
        self.instrument_type = instrument_type

    @property
    def identifiers(self):
        """Gets the identifiers of this ComplexBondAllOf.  # noqa: E501

        external market codes and identifiers for the bond, e.g. ISIN.  # noqa: E501

        :return: The identifiers of this ComplexBondAllOf.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._identifiers

    @identifiers.setter
    def identifiers(self, identifiers):
        """Sets the identifiers of this ComplexBondAllOf.

        external market codes and identifiers for the bond, e.g. ISIN.  # noqa: E501

        :param identifiers: The identifiers of this ComplexBondAllOf.  # noqa: E501
        :type identifiers: dict(str, str)
        """

        self._identifiers = identifiers

    @property
    def calculation_type(self):
        """Gets the calculation_type of this ComplexBondAllOf.  # noqa: E501

        The calculation type applied to the bond coupon amount. This is required for bonds that have a particular type of computing the period coupon, such as simple compounding,  irregular coupons etc.  The default CalculationType is `Standard`, which returns a coupon amount equal to Principal * Coupon Rate / Coupon Frequency. Coupon Frequency is 12M / Payment Frequency.  Payment Frequency can be 1M, 3M, 6M, 12M etc. So Coupon Frequency can be 12, 4, 2, 1 respectively.    Supported string (enumeration) values are: [Standard, DayCountCoupon, NoCalculationFloater, BrazilFixedCoupon].  # noqa: E501

        :return: The calculation_type of this ComplexBondAllOf.  # noqa: E501
        :rtype: str
        """
        return self._calculation_type

    @calculation_type.setter
    def calculation_type(self, calculation_type):
        """Sets the calculation_type of this ComplexBondAllOf.

        The calculation type applied to the bond coupon amount. This is required for bonds that have a particular type of computing the period coupon, such as simple compounding,  irregular coupons etc.  The default CalculationType is `Standard`, which returns a coupon amount equal to Principal * Coupon Rate / Coupon Frequency. Coupon Frequency is 12M / Payment Frequency.  Payment Frequency can be 1M, 3M, 6M, 12M etc. So Coupon Frequency can be 12, 4, 2, 1 respectively.    Supported string (enumeration) values are: [Standard, DayCountCoupon, NoCalculationFloater, BrazilFixedCoupon].  # noqa: E501

        :param calculation_type: The calculation_type of this ComplexBondAllOf.  # noqa: E501
        :type calculation_type: str
        """

        self._calculation_type = calculation_type

    @property
    def schedules(self):
        """Gets the schedules of this ComplexBondAllOf.  # noqa: E501

        schedules.  # noqa: E501

        :return: The schedules of this ComplexBondAllOf.  # noqa: E501
        :rtype: list[lusid.Schedule]
        """
        return self._schedules

    @schedules.setter
    def schedules(self, schedules):
        """Sets the schedules of this ComplexBondAllOf.

        schedules.  # noqa: E501

        :param schedules: The schedules of this ComplexBondAllOf.  # noqa: E501
        :type schedules: list[lusid.Schedule]
        """

        self._schedules = schedules

    @property
    def instrument_type(self):
        """Gets the instrument_type of this ComplexBondAllOf.  # noqa: E501

        The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashFlowsLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap, CashPerpetual, CapFloor, CashSettled, CdsIndex, Basket, FundingLeg, FxSwap, ForwardRateAgreement, SimpleInstrument, Repo, Equity, ExchangeTradedOption, ReferenceInstrument, ComplexBond, InflationLinkedBond, InflationSwap  # noqa: E501

        :return: The instrument_type of this ComplexBondAllOf.  # noqa: E501
        :rtype: str
        """
        return self._instrument_type

    @instrument_type.setter
    def instrument_type(self, instrument_type):
        """Sets the instrument_type of this ComplexBondAllOf.

        The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashFlowsLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap, CashPerpetual, CapFloor, CashSettled, CdsIndex, Basket, FundingLeg, FxSwap, ForwardRateAgreement, SimpleInstrument, Repo, Equity, ExchangeTradedOption, ReferenceInstrument, ComplexBond, InflationLinkedBond, InflationSwap  # noqa: E501

        :param instrument_type: The instrument_type of this ComplexBondAllOf.  # noqa: E501
        :type instrument_type: str
        """
        if self.local_vars_configuration.client_side_validation and instrument_type is None:  # noqa: E501
            raise ValueError("Invalid value for `instrument_type`, must not be `None`")  # noqa: E501
        allowed_values = ["QuotedSecurity", "InterestRateSwap", "FxForward", "Future", "ExoticInstrument", "FxOption", "CreditDefaultSwap", "InterestRateSwaption", "Bond", "EquityOption", "FixedLeg", "FloatingLeg", "BespokeCashFlowsLeg", "Unknown", "TermDeposit", "ContractForDifference", "EquitySwap", "CashPerpetual", "CapFloor", "CashSettled", "CdsIndex", "Basket", "FundingLeg", "FxSwap", "ForwardRateAgreement", "SimpleInstrument", "Repo", "Equity", "ExchangeTradedOption", "ReferenceInstrument", "ComplexBond", "InflationLinkedBond", "InflationSwap"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and instrument_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `instrument_type` ({0}), must be one of {1}"  # noqa: E501
                .format(instrument_type, allowed_values)
            )

        self._instrument_type = instrument_type

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ComplexBondAllOf):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ComplexBondAllOf):
            return True

        return self.to_dict() != other.to_dict()
