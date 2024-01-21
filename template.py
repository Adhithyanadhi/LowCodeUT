from copy import deepcopy
from typing import List
import os
TEST_CASE_ID = 0
CWD = os.getcwd()

# regex to be modified to check dao., utils., service.,
REGEX_OTHER_INTERFACE_FUNC_CALL = r"(((\s|\()(s\.))(.*)(\.)(.*)(\()(.*)(\)))"

class MOCK_FUNC_DICT:
	def __init__(self, interface_name, mock_func_name, mock_func_inputs, mock_func_outputs):
		self.interface_name: str = interface_name
		self.mock_func_name: str = mock_func_name
		self.mock_func_inputs: List[str] =  mock_func_inputs
		self.mock_func_outputs: List[str] =  mock_func_outputs
		if mock_func_name == "Decode":
			self.mock_run : bool = True
		else:
			self.mock_run : bool = False
	def __repr__(self):
		return str(vars(self))
	def __eq__(self, object) -> bool:
		if self is None and object is None:
			return True
		if self is not None and object is not None:     
			return self.interface_name == object.interface_name and \
			self.mock_func_name == object.mock_func_name and \
			self.mock_func_inputs == object.mock_func_inputs and \
			self.mock_func_outputs == object.mock_func_outputs and \
			self.mock_run == object.mock_run 
		return False

class TEST_CASE_DICT:
	def __init__(self, func_name, test_case_id, inputs, expected_outputs, mock_functions):
		self.func_name: str = func_name
		self.test_case_id: int = test_case_id
		self.inputs: List[str] = inputs
		self.expected_outputs: List[str] = expected_outputs
		self.mock_functions: List[MOCK_FUNC_DICT] = [mock_function for mock_function in mock_functions]
		# self.output_changed : bool = False
	def __repr__(self):
		return str(vars(self))
	def __eq__(val1, val2):
		if val1 is None and val2 is None:
			return True
		if val1 is not None and val2 is not None:
			return val1.func_name == val2.func_name and val1.inputs == val2.inputs and val1.expected_outputs == val2.expected_outputs and val1.mock_functions == val2.mock_functions
		return False

TEST_CASE_TEMPLATE = """
	{
		Case: "%s - %s",
		Inputs: []interface{}{
			%s
		},
		ExpectedOutputs: []interface{}{
			%s
		},
		MockFunctions: []func(ctx tapcontext.TContext){
			%s
		},
	},
"""

MOCK_FUNC_TEMPLATE = """
		func(ctx tapcontext.TContext) {
			tests.%s.
				On(
					"%s",
					%s
				).
				Return(
					%s
				).
				%s
		},
"""

OUTPUT_PARAMETER_TEMPLATE = "out%s"
ASSERT_STATEMENT_TEMPLATE = """
fmt.Println("asserting out%s")
if !assert.Equal(t, test.ExpectedOutputs[%s], out%s){
    panic("Not equal output param - out%s, kindly check")
}"""

AssertTemplate = """
		assert.Equal(t, test.ExpectedOutputs[%s], out%s)
"""

TestServiceInputArgumentTemplate = " test.Inputs[%s].(%s)"



TEST_FUNC_TEMPLATE = """
// %s

func Test%s(t *testing.T) {
	Init()
	var ctx = tapcontext.NewTapContext()
	for _, test := range test_cases.%sTestCases {
		fmt.Println("Case - ", test.Case)
		tests.InitializeMockFunctions(test.MockFunctions, ctx)
		%s := %s.%s(ctx, %s)
		%s
	}
}
"""

class UT_TEST_CASES_DICT:
    def __init__(self, func_name, test_cases):
        self.func_name:str = func_name
        self.test_cases: List[TEST_CASE_DICT] = [test_case for test_case in test_cases]
		

UT_TEST_CASES_TEMPLATE = """
package test_cases
import (
	"gitlab.com/tekion/development/tap/backend/taplibgo/tapcontext"
 %s
)
 
// %s
var %sTestCases = []TestCase{
	%s
}
"""




RUN_TEMPLATE = """
				Run(func(args mock.Arguments) {
					arg := args.Get(2).(*map[string]interface{})
					(*arg) = make(map[string]interface{})
					(*arg)["status"] = "Ok"
					(*arg)["message"] = "message"
				}).
				Once()
"""

RUN_ONCE_TEMPLATE = "Once()"


INTERFACE_FILE_NAME_MAP = {
	"CampaignMemberService": "/service/v1/campaign_member.go",
	"CampaignIndustrialConferenceDao": "/service/v1/campaign_industrial_conference.go",
	"CampaignService": "/service/v1/campaign.go",
	"DemoStationService": "/service/v1/demo_station.go",
	"HelperUtils": "/utils/helper_utils.go",
	"HttpRequestUtils": "/utils/http_request.go",
	"CommonUtils": "/utils/common_utils.go",
	"CampaignES": "/es/campaign.go",
	"CampaignMemberES": "/es/campaign_members.go",
	"LeadES": "/es/lead.go",
	"LeadService": "/service/v1/lead_service.go",
	"LeadSourceDao": "/db/lead_source.go",
	"LeadStageDao": "/db/lead_stage.go",
	"CommonDao": "/db/common.go",
	"LeadDao": "/db/lead.go",
	"ProspectsDao": "/db/prospects.go",
	"CampaignMemberIndustrialConferenceDao": "/db/campaign_industrial_conference.go",
	"DemoStationDao": "/db/demo_station.go",
	"CampaignDao": "/db/campaign.go",
	"CampaignScripts": "/scripts/campaign.go",
	"LeadScripts": "/scripts/lead.go",
	"CampaignMemberScripts": "/scripts/campaign_member.go",
}

OUTPUT_POSSIBILITIES = {
	
}

STRUCT_NAME_FILE_MAP = {
	"models": {
		"CampaignIdFormIdMapping": "/models/prospects.go",
		"Campaign": "/models/campaign.go",
		"CampaignPlan": "/models/campaign.go",
		"CampaignActual": "/models/campaign.go",
		"CampaignIntegration": "/models/campaign.go",
		"CampaignType": "/models/campaign.go",
		"CampaignTypeState": "/models/campaign.go",
		"CampaignMember": "/models/campaign.go",
		"CampaignMemberAddress": "/models/campaign.go",
		"CampaignMemberIndustrialConference": "/models/campaign.go",
		"CampaignContactEdit": "/models/campaign.go",
		"CampaignStatus": "/models/campaign.go",
		"CampaignLog": "/models/campaign.go",
		"CampaignAddress": "/models/campaign.go",
		"CampaignMemberLeadMap": "/models/campaign.go",
		"CampaignMemberDemoStationActivityMapping": "/models/campaign.go",
		"CampaignMemberCheckIn": "/models/campaign.go",
		"CampaignDemoEmailRemainder": "/models/campaign.go",
		"CampaignMailEventLog": "/models/campaign.go",
		"CampaignEventMapping": "/models/campaign.go",
		"ExternalDataProviderRequestResponse": "/models/campaign.go",
		"CampaignBasicDetail": "/models/campaign.go",
		"Form": "/models/campaign.go",
		"CCMDemostationData": "/models/campaign.go",
		"CustomField": "/models/custom_fields.go",
		"ModuleCustomField": "/models/custom_fields.go",
		"CampaignCustomField": "/models/custom_fields.go",
		"CampaignCustomFieldData": "/models/custom_fields.go",
		"CustomFieldModel": "/models/custom_fields.go",
		"LeadCustomField": "/models/custom_fields.go",
		"LeadCustomFieldData": "/models/custom_fields.go",
		"DemoStation": "/models/demo_station.go",
		"DemoStationFilter": "/models/demo_station.go",
		"FormExternalRequest": "/models/prospects.go",
		"CampaignIdFormIdMapping": "/models/prospects.go",
		"CampaignMemberStateTransitionEmail": "/models/prospects.go",
		"CampaignMemberDetails": "/models/prospects.go",
	},
	"resources": {
		"CampaignMemberFilterResponse": "/resources/campaign.go",
		"CampaignFilterResponse": "/resources/campaign.go",
		"CampaignInputField": "/resources/campaign.go",
		"CampaignPlan": "/resources/campaign.go",
		"CampaignActual": "/resources/campaign.go",
		"CampaignIntegration": "/resources/campaign.go",
		"CampaignType": "/resources/campaign.go",
		"CampaignTypeState": "/resources/campaign.go",
		"CampaignFilterResponse": "/resources/campaign.go",
		"CampaignMemberInput": "/resources/campaign.go",
		"ParentCampaignMemberInput": "/resources/campaign.go",
		"CampaignMemberAddress": "/resources/campaign.go",
		"CampaignMemberIndustrialConference": "/resources/campaign.go",
		"CampaignContactEdit": "/resources/campaign.go",
		"CampaignBasicDetail": "/resources/campaign.go",
		"CampaignAddress": "/resources/campaign.go",
		"DeleteContactMembersInput": "/resources/campaign.go",
		"WebinarRegistrant": "/resources/campaign.go",
		"WebinarParticipant": "/resources/campaign.go",
		"WebinarAbsentee": "/resources/campaign.go",
		"FormExternalDataAndCCM": "/resources/campaign.go",
		"CreateContactForIndustryConference": "/resources/campaign.go",
		"CreateContactEmailRequest": "/resources/campaign.go",
		"CreateContactAccountOwnerRequest": "/resources/campaign.go",
		"CheckInInput": "/resources/campaign.go",
		"TimeSlot": "/resources/campaign.go",
		"CampaignTime": "/resources/campaign.go",
		"Followup": "/resources/campaign.go",
		"NoShow": "/resources/campaign.go",
		"CampaignDemoEmailRemainder": "/resources/campaign.go",
		"DemoRemainderActivityData": "/resources/campaign.go",
		"ProductTypeList": "/resources/campaign.go",
		"CreateContactAddressRequest": "/resources/campaign.go",
		"CreateContactPhoneRequest": "/resources/campaign.go",
		"NadaProspectWalkIn": "/resources/campaign.go",
		"NadaProspectWalkInResponseMessage": "/resources/campaign.go",
		"NadaProspectWalkInResponseLeadInfo": "/resources/campaign.go",
		"NadaProspectWalkInResponseDemographics": "/resources/campaign.go",
		"NadaProspectWalkInResponse": "/resources/campaign.go",
		"CampaignFilter": "/resources/campaign.go",
		"ContactEmailDetails": "/resources/campaign.go",
		"ContactBasicInfoResponse": "/resources/campaign.go",
		"ActivityDemo": "/resources/campaign.go",
		"NadaLeadWalkInWeb": "/resources/campaign.go",
		"CampaignFollowUpEmailTrigger": "/resources/campaign.go",
		"ActivityFeedbackUpdate": "/resources/campaign.go",
		"GenericGetKeyValue": "/resources/campaign.go",
		"GenericUpdate": "/resources/campaign.go",
		"ThankYouEmailTrigger": "/resources/campaign.go",
		"TapCalenderUser": "/resources/campaign.go",
		"Campaign": "/resources/campaign.go",
		"CampaignDetails": "/resources/campaign.go",
		"CampaignIdStatus": "/resources/campaign.go",
		"CampaignMemberWithDemoStation": "/resources/campaign.go",
		"FilteredContactsResponse": "/resources/campaign.go",
		"CampaignMemberFilterResponse": "/resources/campaign.go",
		"AllCampaignMembers": "/resources/campaign.go",
		"AssociatedIDAndAccountID": "/resources/campaign.go",
		"AssociatedTableIDsForMergingAccountID": "/resources/campaign.go",
		"MergeCampaignMember": "/resources/campaign.go",
		"CampaignMemberContact": "/resources/campaign.go",
		"CampaignMemberWithParentChild": "/resources/campaign.go",
		"CampaignMemberDemoStationActivityMapping": "/resources/campaign.go",
		"CampaignMemberLeadMap": "/resources/campaign.go",
		"CampaignMember": "/resources/campaign.go",
		"ServiceError": "/resources/common.go",
		"ServiceResult": "/resources/common.go",
		"ServiceResultData": "/resources/common.go",
		"ResponseData": "/resources/common.go",
		"Region": "/resources/common.go",
		"CodedResponse": "/resources/common.go",
		"CaptchaPayload": "/resources/common.go",
		"CodedServiceResponse": "/resources/common.go",
		"CreateActivityFeedbackPayload": "/resources/common.go",
		"TMCommonNotificationInput": "/resources/common.go",
		"KafkaProducerContent": "/resources/common.go",
		"PusherData": "/resources/common.go",
		"LeadAssociation": "/resources/common.go",
		"CampaignAssociation": "/resources/common.go",
		"TeamsNotificationPayload": "/resources/common.go",
		"CustomField": "/resources/custom_fields.go",
		"CustomFieldValue": "/resources/custom_fields.go",
		"DemoStation": "/resources/demo_station.go",
		"EventFields": "/resources/demo_station.go",
		"Events": "/resources/demo_station.go",
		"EventMembership": "/resources/demo_station.go",
		"EventProfile": "/resources/demo_station.go",
		"EventCategory": "/resources/demo_station.go",
		"PeopleFilter": "/resources/demo_station.go",
		"PeopleFilterResult": "/resources/demo_station.go",
		"CalendarEventUUIDs": "/resources/demo_station.go",
		"SMEmailActFBUUID": "/resources/demo_station.go",
		"CampaignIdFormIdMapping": "/resources/prospects.go",
		"CampaignProspectInput": "/resources/prospects.go",
		"Response": "/resources/prospects.go",
		"CampaignMemberCheckIn": "/resources/prospects.go",
		"CampaignMemberDetails": "/resources/prospects.go",
		"FormSubmissionEmailBody": "/resources/prospects.go",
		"CcBcc": "/resources/prospects.go",
		"CampaignFormUUIDs": "/resources/prospects.go",
		"FormProspect": "/resources/prospects.go",
}
}

MOCK_BEGIN_TRANSACTION = MOCK_FUNC_DICT(interface_name="MockTx", mock_func_name="BeginTransaction", mock_func_inputs=[], mock_func_outputs=["txObj"])
MOCK_ADD_TRANSACTOR_TO_CONTEXT = MOCK_FUNC_DICT(interface_name="MockTx", mock_func_name="AddTransactorToContext", mock_func_inputs=["ctx", "txObj"], mock_func_outputs=["ctx"])
MOCK_GET_EXISTING_TRANSACTOR_FROM_CONTEXT = MOCK_FUNC_DICT(interface_name="MockTx", mock_func_name='GetExistingTransactorFromContext', mock_func_inputs=["ctx"], mock_func_outputs=["txObj"])

