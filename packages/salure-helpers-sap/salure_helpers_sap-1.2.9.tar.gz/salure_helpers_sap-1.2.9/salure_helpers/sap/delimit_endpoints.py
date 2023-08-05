from salure_helpers.sap.base_functions import BaseFunctions
import requests


class DelimitEndpoints:
    def __init__(self, label: str, data_dir: str, certificate_file: str = None, key_file: str = None, debug: bool = False):
        self.base_class = BaseFunctions(label=label, data_dir=data_dir, certificate_file=certificate_file, key_file=key_file, debug=debug)
        self.data_dir = data_dir
        self.debug = debug

    def delimit_master_action(self, employee_id, start_date, end_date):
        """
        Delimit personal data
        :param employee_id: the ID of the employee you want to delimit
        :param start_date: the start date of the record you want to delimit
        :param end_date: the end date at which the record will be delimit
        :return: status
        """
        data_filter = f"Afasemployeenumber='{employee_id}',Startdate='{start_date}',Enddate='{end_date}'"
        response = self.base_class.delete_data(uri='MasterActionDel', filter=data_filter)
        response.raise_for_status()
        return response

    def delimit_org_unit(self, org_unit, start_date, end_date):
        """
        Delimit organisational units
        :param org_unit: the ID of the organisational unit you want to delimit
        :param start_date: the start date of the record you want to delimit
        :param end_date: the end date at which the record will be delimit
        :return: status
        """
        data_filter = f"OrgUnitID='{org_unit}',Startdate='{start_date}',Enddate='{end_date}'"
        response = self.base_class.delete_data(uri='OrgUnitDel', filter=data_filter)
        response.raise_for_status()
        return response

    def delimit_position(self, position_id, start_date, end_date):
        """
        Delimit positions in SAP
        :param position_id: the ID of the organisational unit you want to delimit
        :param start_date: the start date of the record you want to delimit
        :param end_date: the end date at which the record will be delimit
        :return: status
        """
        data_filter = f"PositionID='{position_id}',Startdate='{start_date}',Enddate='{end_date}'"
        response = self.base_class.delete_data(uri="PositionDel", filter=data_filter)
        response.raise_for_status()
        return response

    def delete_workcenter(self, position_id, start_date, end_date, workcenter):
        """
        Delimit positions in SAP
        :param position_id: the ID of the organisational unit you want to delimit
        :param start_date: the start date of the record you want to delimit
        :param end_date: the end date at which the record will be delimit
        :param workcenter: the workcenter you want to delimit
        :return: status
        """
        data_filter = f"PositionID='{position_id}',Startdate='{start_date}',Enddate='{end_date}',WorkcenterID='{workcenter}'"
        response = self.base_class.delete_data(uri="WorkcenterDel", filter=data_filter)
        response.raise_for_status()
        return response
