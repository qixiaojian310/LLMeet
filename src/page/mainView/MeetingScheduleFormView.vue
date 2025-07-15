<template>
  <Form
    v-slot="$form"
    :initialValues
    :resolver
    class="form"
    @submit="
      e => {
        loading = true;
        onFormSubmit(e);
        loading = false;
      }
    "
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
        <Message v-if="$form.meetingTitle?.invalid" severity="error" size="small" variant="simple">
          {{ $form.meetingTitle.error?.message }}
        </Message>
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
        <Message v-if="$form.meetingTitle?.invalid" severity="error" size="small" variant="simple">
          {{ $form.meetingTitle.error?.message }}
        </Message>
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
          hour-format="24"
        />
        <label for="meetingStartTime">Meeting Start Time</label>
        <Message
          v-if="$form.meetingStartTime?.invalid"
          severity="error"
          size="small"
          variant="simple"
        >
          {{ $form.meetingStartTime.error?.message }}
        </Message>
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
            <Button label="Customize Time" fluid severity="secondary" icon="pi pi-plus" />
          </template>
        </Select>
        <label for="meetingDuration">Meeting Duration</label>

        <Message
          v-if="$form.meetingDuration?.invalid"
          severity="error"
          size="small"
          variant="simple"
        >
          {{ $form.meetingDuration.error?.message }}
        </Message>
      </IftaLabel>
    </div>
    <Button type="submit" severity="secondary" :disabled="loading">
      <FontAwesomeIcon :icon="faChampagneGlasses" />
      Enter Meeting
    </Button>
  </Form>
</template>

<script setup lang="ts">
import { Form, FormSubmitEvent } from '@primevue/forms';
import { Button, IftaLabel, InputText, Message, DatePicker, Select } from 'primevue';
import { reactive, ref } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faChampagneGlasses } from '@fortawesome/free-solid-svg-icons';
import { message } from 'ant-design-vue';
import { createMeeting, MeetingInfo } from '@/request/meeting';
const initialValues = reactive({
  username: '',
  meetingTitle: '',
  meetingDescription: '',
  meetingStartTime: new Date(),
  meetingDuration: 30
});

const durationOptions = reactive([
  { label: '30 minutes', value: 30 },
  { label: '1 hour', value: 60 },
  { label: '2 hours', value: 120 }
]);

const loading = ref(false);

const resolver = ({ values }: any) => {
  const errors: any = {};

  if (!values.username) {
    errors.username = [{ message: 'Username is required.' }];
  }
  if (!values.meetingTitle) {
    errors.meetingTitle = [{ message: 'Meeting number is required.' }];
  }
  if (!values.meetingDescription) {
    errors.meetingDescription = [{ message: 'Meeting description is required.' }];
  }
  if (values.meetingTitle.length > 225) {
    errors.meetingDescription = [{ message: 'Meeting title is too long.' }];
  }

  return {
    values, // (Optional) Used to pass current form values to submit event.
    errors
  };
};

const onFormSubmit = async ({ valid, values }: FormSubmitEvent) => {
  if (!valid) return;

  // 构造请求参数
  const startTime = new Date(values.meetingStartTime);
  const endTime = new Date(startTime.getTime() + values.meetingDuration * 60 * 1000);

  const sendRequest: MeetingInfo = {
    title: values.meetingTitle,
    description: values.meetingDescription,
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString()
  };

  const res = await createMeeting(sendRequest);
  // 创建失败
  if (typeof res === 'number') {
    message.error('Meeting creation failed');
    return;
  }

  // 不加入会议，仅预定
  if (!values.joinMeeting) {
    message.success('Meeting scheduled successfully');
    return;
  }
};
</script>

<style scoped lang="scss">
.form {
  overflow: auto;
  align-items: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
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
