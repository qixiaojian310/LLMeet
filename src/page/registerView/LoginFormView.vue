<template>
  <Form
    v-slot="$form"
    :initialValues
    :resolver
    @submit="onFormSubmit"
    class="form"
  >
    <div class="title">Start meeting with LLMeet</div>

    <div class="form-text">
      <IftaLabel>
        <InputText
          id="username"
          name="username"
          type="text"
          placeholder="Username"
          fluid
        />
        <label for="username">Username</label>
        <Message
          v-if="$form.username?.invalid"
          severity="error"
          size="small"
          variant="simple"
          >{{ $form.username.error?.message }}</Message
        >
      </IftaLabel>
    </div>
    <div class="form-text">
      <IftaLabel>
        <InputText
          id="password"
          name="password"
          type="password"
          placeholder="Password"
          fluid
        />
        <label for="password">Password</label>

        <Message
          v-if="$form.password?.invalid"
          severity="error"
          size="small"
          variant="simple"
          >{{ $form.password.error?.message }}</Message
        >
      </IftaLabel>
    </div>
    <!-- <div class="form-check-box">
      <div class="form-check">
        <RadioButton name="registerOption" inputId="remember" value="rememberPassword" />
        <label for="rememberPassword">Remember Password</label>
      </div>
    </div> -->
    <Toast />
    <Button type="submit" severity="secondary">
      <FontAwesomeIcon :icon="fas.faChampagneGlasses" />
      Login
    </Button>
  </Form>
</template>

<script setup lang="ts">
import { Form, FormSubmitEvent } from "@primevue/forms";
import { Button, IftaLabel, InputText, Message, Toast } from "primevue";
import { reactive } from "vue";
import { useToast } from "primevue/usetoast";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { fas } from "@fortawesome/free-solid-svg-icons";
import { signin } from "@/request/authorization";
import { router } from "@/router";

const toast = useToast();

const initialValues = reactive({
  username: "",
  password: "",
});

const resolver = ({ values }: any) => {
  const errors: any = {};

  if (!values.username) {
    errors.username = [{ message: "Username is required." }];
  }
  if (!values.password) {
    errors.password = [{ message: "Password is required." }];
  }

  return {
    values, // (Optional) Used to pass current form values to submit event.
    errors,
  };
};

const onFormSubmit = async (e: FormSubmitEvent) => {
  if (e.valid) {
    const res = await signin({
      username: e.values.username,
      password: e.values.password,
    });
    if (typeof res !== "number") {
      toast.add({
        severity: "success",
        summary: "Login successful.",
        life: 3000,
      });
      router.push({ path: "/home" });
    } else {
      toast.add({
        severity: "error",
        summary: "Login failed.",
        detail: "Username or password is incorrect.",
      });
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
  justify-content: center;

  .title {
    color: #ffffff;
    font-size: 32px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
  }

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
