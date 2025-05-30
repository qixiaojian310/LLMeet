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
          id="meetingNumber"
          name="meetingNumber"
          type="text"
          placeholder="Meeting number"
          fluid
        />
        <label for="meetingNumber">Meeting Number</label>

        <Message
          v-if="$form.meetingNumber?.invalid"
          severity="error"
          size="small"
          variant="simple"
          >{{ $form.meetingNumber.error?.message }}</Message
        >
      </IftaLabel>
    </div>
    <div class="form-text">
      <IftaLabel>
        <InputText
          id="username"
          name="username"
          type="text"
          placeholder="Username"
          fluid
        />
        <label for="username">Your meeting name</label>
        <Message
          v-if="$form.username?.invalid"
          severity="error"
          size="small"
          variant="simple"
          >{{ $form.username.error?.message }}</Message
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
import { Button, IftaLabel, InputText, Message, Checkbox } from "primevue";
import { reactive } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { fas } from "@fortawesome/free-solid-svg-icons";
import { router } from "@/router";
import { notification } from "ant-design-vue";
import { useUserStore } from "@/stores/userStore";
import { onMounted } from "vue";
import { getMeeting, getMeetingToken } from "@/request/meeting";
import { useMeetingStore } from "@/stores/meetingStore";

const userStore = useUserStore();
const meetingStore = useMeetingStore();
const initialValues = reactive({
  username: userStore.username,
  meetingNumber: "",
  meetingOption: [],
});

const resolver = ({ values }: any) => {
  const errors: any = {};

  if (!values.username) {
    errors.username = [{ message: "Username is required." }];
  }
  if (!values.meetingNumber) {
    errors.meetingNumber = [{ message: "Meeting number is required." }];
  }

  return {
    values, // (Optional) Used to pass current form values to submit event.
    errors,
  };
};

const onFormSubmit = async ({ valid, values }: FormSubmitEvent) => {
  if (valid) {
    const res = await getMeeting(values.meetingNumber);
    if (!res.success) {
      notification.error({
        message: "Meeting not found",
        description: "Please check your meeting number",
      });
      return;
    }
    const tokenRes = await getMeetingToken(
      values.meetingNumber,
      values.username
    );
    if (typeof tokenRes !== "number") {
      meetingStore.setMeetingInfo({
        meetingId: res.meeting.meetingId,
        meetingToken: tokenRes.token,
        meetingName: res.meeting.title,
        description: res.meeting.description,
        startTime: new Date(res.meeting.startTime)
          .toISOString()
          .slice(0, 19)
          .replace("T", " "),
        endTime: new Date(res.meeting.endTime)
          .toISOString()
          .slice(0, 19)
          .replace("T", " "),
        createTime: new Date(res.meeting.createdAt)
          .toISOString()
          .slice(0, 19)
          .replace("T", " "),
      });
      router.push("/meeting");
      notification.success({
        message: "Meeting entered successfully",
        description: "You can now enter the meeting",
      });
    } else {
      notification.error({
        message: "Meeting token generation failed",
        description: "Please try again",
      });
    }
  }
};

onMounted(() => {
  console.log("form mounted", userStore.username);
});
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
