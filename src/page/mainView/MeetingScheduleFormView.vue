<template>
  <Form
    v-slot="$form"
    :initialValues
    :resolver
    @submit="onFormSubmit"
    class="form"
  >
    <div class="form-text">
      <IftaLabel>
        <InputText
          id="meetingTitle"
          name="meetingTitle"
          type="text"
          placeholder="Meeting name"
          fluid
        />
        <label for="meetingTitle">Meeting Name</label>
        <Message
          v-if="$form.meetingTitle?.invalid"
          severity="error"
          size="small"
          variant="simple"
          >{{ $form.meetingTitle.error?.message }}</Message
        >
      </IftaLabel>
    </div>
    <div class="form-text">
      <IftaLabel>
        <InputText
          id="meetingDescription"
          name="meetingDescription"
          style="width: 100%; resize: none; font-size: 1rem"
          type="text"
          fluid
        />
        <label for="meetingDescription">Meeting Description</label>
        <Message
          v-if="$form.meetingTitle?.invalid"
          severity="error"
          size="small"
          variant="simple"
          >{{ $form.meetingTitle.error?.message }}</Message
        >
      </IftaLabel>
    </div>
    <div class="form-text">
      <IftaLabel>
        <DatePicker
          id="meetingStartTime"
          name="meetingStartTime"
          type="text"
          placeholder="Meeting number"
          fluid
          show-time
          hourFormat="24"
        />
        <label for="meetingStartTime">Meeting Start Time</label>
        <Message
          v-if="$form.meetingStartTime?.invalid"
          severity="error"
          size="small"
          variant="simple"
          >{{ $form.meetingStartTime.error?.message }}</Message
        >
      </IftaLabel>
    </div>
    <div class="form-text">
      <IftaLabel>
        <Select
          label-id="meetingDuration"
          name="meetingDuration"
          :options="durationOptions"
          option-label="label"
          option-value="value"
          fluid
        >
          <template #footer>
            <Button
              label="Customize Time"
              fluid
              severity="secondary"
              icon="pi pi-plus"
            ></Button>
          </template>
        </Select>
        <label for="meetingDuration">Meeting Duration</label>

        <Message
          v-if="$form.meetingDuration?.invalid"
          severity="error"
          size="small"
          variant="simple"
          >{{ $form.meetingDuration.error?.message }}</Message
        >
      </IftaLabel>
    </div>
    <div class="form-check-box">
      <p>Meeting option</p>
      <div class="form-check">
        <Checkbox
          id="openMic"
          name="meetingOption"
          inputId="openMic"
          value="openMic"
        />
        <label for="openMic">Open Mic</label>
      </div>
      <div class="form-check">
        <Checkbox
          id="openCamera"
          name="meetingOption"
          inputId="openCamera"
          value="openCamera"
        />
        <label for="openCamera">Open Camera</label>
      </div>
    </div>
    <Button type="submit" severity="secondary">
      <FontAwesomeIcon :icon="fas.faChampagneGlasses" />
      Enter Meeting
    </Button>
  </Form>
</template>

<script setup lang="ts">
import { Form, FormSubmitEvent } from "@primevue/forms";
import {
  Button,
  IftaLabel,
  InputText,
  Message,
  Checkbox,
  DatePicker,
  Select,
} from "primevue";
import { reactive } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { fas } from "@fortawesome/free-solid-svg-icons";
import { router } from "@/router";
import { message } from "ant-design-vue";
import { createMeeting, deleteMeeting, getMeetingToken, MeetingInfo, startBot } from "@/request/meeting";
import { useUserStore } from "@/stores/userStore";
import { useMeetingStore } from "@/stores/meetingStore";

const userStore = useUserStore();
const meetingStore = useMeetingStore();
const initialValues = reactive({
  username: "",
  meetingTitle: "",
  meetingDescription: "",
  meetingStartTime: new Date(),
  meetingDuration: 30,
});

const durationOptions = reactive([
  { label: "30 minutes", value: 30 },
  { label: "1 hour", value: 60 },
  { label: "2 hours", value: 120 },
]);

const resolver = ({ values }: any) => {
  const errors: any = {};

  if (!values.username) {
    errors.username = [{ message: "Username is required." }];
  }
  if (!values.meetingTitle) {
    errors.meetingTitle = [{ message: "Meeting number is required." }];
  }
  if (!values.meetingDescription) {
    errors.meetingDescription = [
      { message: "Meeting description is required." },
    ];
  }
  if (values.meetingTitle.length > 225) {
    errors.meetingDescription = [{ message: "Meeting title is too long." }];
  }

  return {
    values, // (Optional) Used to pass current form values to submit event.
    errors,
  };
};

const onFormSubmit = async ({ valid, values }: FormSubmitEvent) => {
  if (valid) {
    //转换时间
    const sendRequest: MeetingInfo = {
      title: values.meetingTitle,
      description: values.meetingDescription,
      startTime: new Date(values.meetingStartTime).toISOString(),
      endTime: new Date(
        values.meetingStartTime.getTime() + values.meetingDuration * 60 * 1000
      ).toISOString(),
    };
    const res = await createMeeting(sendRequest);    
    if (typeof res !== "number") {
      //获取meeting的token->livekit server sdk
      const meetingId = res.meetingId;
      const tokenRes = await getMeetingToken(meetingId, userStore.username);
      // 加入python bot
      const startBotRes = await startBot( meetingId);
      console.log(startBotRes);
      if (typeof tokenRes !== "number") {
        message.success("Meeting created successfully");
        meetingStore.setMeetingInfo({
          meetingId: meetingId,
          meetingToken: tokenRes.token,
          meetingName: values.meetingTitle,
          description: values.meetingDescription,
          startTime: new Date(sendRequest.startTime).toISOString().slice(0, 19).replace('T', ' '),
          endTime: new Date(sendRequest.endTime).toISOString().slice(0, 19).replace('T', ' '),
          createTime: new Date(res.createTime).toISOString().slice(0, 19).replace('T', ' '),
        })
        router.push({ name: "MeetingView" });
      } else {
        message.error("Meeting token generation failed");
        //撤回会议数据库的添加
        const res = await deleteMeeting(meetingId);
        if (res.success){
          message.success("Meeting deleted successfully")
        }
      }
    } else {
      message.error("Meeting creation failed");
    }
  }
};
</script>

<style scoped lang="scss">
.form {
  overflow: auto;
  align-items: center;
  display: flex;
  flex-direction: column;
  gap: 10px;
  height: 100%;

  .form-text {
    width: 60%;
    max-width: 800px;
  }

  .form-check-box {
    color: #ffffff;
    width: 60%;
    max-width: 800px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-items: start;

    .form-check {
      display: flex;
      gap: 10px;
      align-items: center;
    }
  }
}
</style>
