<template>
  <Form v-slot="$form" :initialValues :resolver @submit="onFormSubmit" class="form">
    <div class="form-text">
      <IftaLabel>
        <InputText id="meetingName" name="meetingName" type="text" placeholder="Meeting number" fluid />
        <label for="meetingName">Meeting Name</label>
        <Message v-if="$form.meetingName?.invalid" severity="error" size="small" variant="simple">{{
          $form.meetingName.error?.message }}</Message>
      </IftaLabel>
    </div>
    <div class="form-text">
      <IftaLabel>
        <DatePicker id="meetingStartTime" name="meetingStartTime" type="text" placeholder="Meeting number" fluid
          show-time hourFormat="24" />
        <label for="meetingStartTime">Meeting Start Time</label>
        <Message v-if="$form.meetingStartTime?.invalid" severity="error" size="small" variant="simple">{{
          $form.meetingStartTime.error?.message }}</Message>
      </IftaLabel>
    </div>
    <div class="form-text">
      <IftaLabel>
        <Select label-id="meetingDuration" name="meetingDuration" :options="['30 minutes', '1 hour', '2 hours']" fluid>
          <template #footer>
            <Button label="Customize Time" fluid severity="secondary" icon="pi pi-plus"></Button>
          </template>
        </Select>
        <label for="meetingDuration">Meeting Duration</label>

        <Message v-if="$form.meetingDuration?.invalid" severity="error" size="small" variant="simple">{{
          $form.meetingDuration.error?.message }}</Message>
      </IftaLabel>
    </div>
    <div class="form-check-box">
      <p>Meeting option</p>
      <div class="form-check">
        <Checkbox id="openMic" name="meetingOption" inputId="openMic" value="openMic" />
        <label for="openMic">Open Mic</label>
      </div>
      <div class="form-check">
        <Checkbox id="openCamera" name="meetingOption" inputId="openCamera" value="openCamera" />
        <label for="openCamera">Open Camera</label>
      </div>
    </div>
    <Toast />
    <Button type="submit" severity="secondary">
      <FontAwesomeIcon :icon="fas.faChampagneGlasses" />
      Enter Meeting
    </Button>
  </Form>
</template>

<script setup lang="ts">

import { Form } from '@primevue/forms';
import { Button, IftaLabel, InputText, Message, Toast, Checkbox, DatePicker, Select } from 'primevue';
import { reactive } from 'vue';
import { useToast } from 'primevue/usetoast';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';

const toast = useToast();

const initialValues = reactive({
  username: '',
  meetingName: '',
  meetingStartTime: new Date(),
  meetingDuration: "30 minutes",
});

const resolver = ({ values }: any) => {
  const errors: any = {};

  if (!values.username) {
    errors.username = [{ message: 'Username is required.' }];
  }
  if (!values.meetingName) {
    errors.meetingName = [{ message: 'Meeting number is required.' }];
  }

  return {
    values, // (Optional) Used to pass current form values to submit event.
    errors
  };
};

const onFormSubmit = ({ valid }: any) => {
  if (valid) {
    toast.add({
      severity: 'success',
      summary: 'Form is submitted.',
      life: 3000
    });
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