<template>
  <Form v-slot="$form" :initialValues :resolver class="form" @submit="onFormSubmit">
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

        <Message v-if="$form.meetingNumber?.invalid" severity="error" size="small" variant="simple">
          {{ $form.meetingNumber.error?.message }}
        </Message>
      </IftaLabel>
    </div>
    <div class="form-text">
      <IftaLabel>
        <InputText id="username" name="username" type="text" placeholder="Username" fluid />
        <label for="username">Your meeting name</label>
        <Message v-if="$form.username?.invalid" severity="error" size="small" variant="simple">
          >
          {{ $form.username.error?.message }}
        </Message>
      </IftaLabel>
    </div>
    <div class="form-check-box">
      <p>Meeting option</p>
      <div class="form-check">
        <Checkbox id="openMic" name="meetingOption" input-id="openMic" value="openMic" />
        <label for="openMic">Open Mic</label>
      </div>
      <div class="form-check">
        <Checkbox id="openCamera" name="meetingOption" input-id="openCamera" value="openCamera" />
        <label for="openCamera">Open Camera</label>
      </div>
    </div>
    <Button type="submit" severity="secondary">
      <FontAwesomeIcon :icon="faChampagneGlasses" />
      Enter Meeting
    </Button>
  </Form>
</template>

<script setup lang="ts">
import { Form, FormSubmitEvent } from '@primevue/forms';
import { Button, IftaLabel, InputText, Message, Checkbox } from 'primevue';
import { reactive } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faChampagneGlasses } from '@fortawesome/free-solid-svg-icons';
import { router } from '@/router';
import { useUserStore } from '@/stores/userStore';
import { onMounted } from 'vue';
import { getMeeting, getMeetingToken, joinMeeting } from '@/request/meeting';
import { useMeetingStore } from '@/stores/meetingStore';
import { message } from 'ant-design-vue';
import { useRecordStore } from '@/stores/recordStore';

const userStore = useUserStore();
const meetingStore = useMeetingStore();
const recordStore = useRecordStore();
const initialValues = reactive({
  username: userStore.username,
  meetingNumber: '',
  meetingOption: []
});

const resolver = ({ values }: any) => {
  const errors: any = {};

  if (!values.username) {
    errors.username = [{ message: 'Username is required.' }];
  }
  if (!values.meetingNumber) {
    errors.meetingNumber = [{ message: 'Meeting number is required.' }];
  }

  return {
    values, // (Optional) Used to pass current form values to submit event.
    errors
  };
};

const onFormSubmit = async ({ valid, values }: FormSubmitEvent) => {
  if (valid) {
    const res = await getMeeting(values.meetingNumber);
    if (!res.success) {
      message.error('Meeting not found');
      return;
    }
    const tokenRes = await getMeetingToken(values.meetingNumber, values.username);
    if (typeof tokenRes === 'number') {
      message.error('Meeting token generation failed');
      return;
    }
    const joinRes = await joinMeeting(values.meetingNumber);
    if (typeof joinRes === 'number') {
      message.error('Meeting join failed');
      return;
    }
    meetingStore.setMeetingInfo({
      meeting_id: res.meeting.meeting_id,
      meetingToken: tokenRes.token,
      meetingName: res.meeting.title,
      description: res.meeting.description,
      start_time: new Date(res.meeting.start_time).toISOString().slice(0, 19).replace('T', ' '),
      end_time: new Date(res.meeting.end_time).toISOString().slice(0, 19).replace('T', ' '),
      create_time: new Date(res.meeting.created_at).toISOString().slice(0, 19).replace('T', ' ')
    });
    recordStore.recordVideo(res.meeting.meeting_id);
    router.push('/meeting');
    message.success('Meeting entered successfully');
  }
};

onMounted(() => {
  console.log('form mounted', userStore.username);
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
    color: var(--primary-text-color);
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
