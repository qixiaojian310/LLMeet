<template>
  <Form v-slot="$form" :initialValues :resolver @submit="onFormSubmit">
    <div>
      <InputText name="meetingNumber" type="text" placeholder="Meeting number" fluid />
      <InputText name="username" type="text" placeholder="Username" fluid />
      <Message v-if="$form.username?.invalid" severity="error" size="small" variant="simple">{{
        $form.username.error?.message }}</Message>
      <Toast />
    </div>
    <Button type="submit" severity="secondary" label="Submit" />
  </Form>
</template>

<script setup lang="ts">

import { Form } from '@primevue/forms';
import { Button, InputText, Message, Toast } from 'primevue';
import { reactive } from 'vue';
import { useToast } from 'primevue/usetoast';

const toast = useToast();

const initialValues = reactive({
  username: '',
  meetingNumber: ''
});

const resolver = ({ values }: any) => {
  const errors: any = {};

  if (!values.username) {
    errors.username = [{ message: 'Username is required.' }];
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

<style scoped></style>