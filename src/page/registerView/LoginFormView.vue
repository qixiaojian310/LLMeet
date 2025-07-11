<template>
  <Form v-slot="$form" :initialValues :resolver class="form" @submit="onFormSubmit">
    <div class="title">Start meeting with LLMeet</div>

    <div class="form-text">
      <IftaLabel>
        <InputText id="username" name="username" type="text" placeholder="Username" fluid />
        <label for="username">Username</label>
        <Message v-if="$form.username?.invalid" severity="error" size="small" variant="simple">
          >
          {{ $form.username.error?.message }}
        </Message>
      </IftaLabel>
    </div>
    <div class="form-text">
      <IftaLabel>
        <InputText id="password" name="password" type="password" placeholder="Password" fluid />
        <label for="password">Password</label>

        <Message v-if="$form.password?.invalid" severity="error" size="small" variant="simple">
          >
          {{ $form.password.error?.message }}
        </Message>
      </IftaLabel>
    </div>
    <div class="form-check-box">
      <div class="goto-link">
        <Button
          variant="link"
          @click="
            () => {
              router.push({ name: 'RegisterForm' });
            }
          "
        >
          Go to register
        </Button>
      </div>
    </div>
    <Button type="submit" severity="secondary">
      <FontAwesomeIcon :icon="faChampagneGlasses" />
      Login
    </Button>
  </Form>
</template>

<script setup lang="ts">
import { Form, FormSubmitEvent } from '@primevue/forms';
import { Button, IftaLabel, InputText, Message } from 'primevue';
import { reactive } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faChampagneGlasses } from '@fortawesome/free-solid-svg-icons';
import { setTimezone, signin } from '@/request/authorization';
import { router } from '@/router';
import { message } from 'ant-design-vue';
import { useUserStore } from '@/stores/userStore';

const initialValues = reactive({
  username: '',
  password: ''
});

const resolver = ({ values }: any) => {
  const errors: any = {};

  if (!values.username) {
    errors.username = [{ message: 'Username is required.' }];
  }
  if (!values.password) {
    errors.password = [{ message: 'Password is required.' }];
  }

  return {
    values, // (Optional) Used to pass current form values to submit event.
    errors
  };
};

const userStore = useUserStore();

const onFormSubmit = async (e: FormSubmitEvent) => {
  if (e.valid) {
    const loginRes = await signin({
      username: e.values.username,
      password: e.values.password
    });
    if (typeof loginRes === 'number') {
      message.error('Login failed, please check your username and password');
      return;
    }
    userStore.login(e.values.username);
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const timezoneRes = await setTimezone(timezone);
    if (typeof timezoneRes === 'number') {
      message.error('Set timezone failed, please try again');
      return;
    }
    router.push({ path: '/home' });
    message.success('Login successful');
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
  justify-content: center;

  .title {
    color: var(--primary-text-color);
    font-size: 2rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
  }

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

    .goto-link {
      width: 100%;
      display: flex;
      justify-content: end;
    }

    .form-check {
      display: flex;
      gap: 10px;
      align-items: center;
    }
  }
}
</style>
