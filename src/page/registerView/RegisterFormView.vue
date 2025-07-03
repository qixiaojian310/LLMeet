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
    <div class="form-text">
      <IftaLabel>
        <InputText
          id="repeatPassword"
          name="repeatPassword"
          type="password"
          placeholder="Repeat Password"
          fluid
        />
        <label for="password">Repeat Password</label>

        <Message
          v-if="$form.repeatPassword?.invalid"
          severity="error"
          size="small"
          variant="simple"
          >{{ $form.repeatPassword.error?.message }}</Message
        >
      </IftaLabel>
    </div>
    <div class="form-text">
      <IftaLabel>
        <InputText
          id="email"
          name="email"
          placeholder="Email"
          fluid
        />
        <label for="email">Email</label>

        <Message
          v-if="$form.email?.invalid"
          severity="error"
          size="small"
          variant="simple"
          >{{ $form.email.error?.message }}</Message
        >
      </IftaLabel>
    </div>
    <div class="form-check-box">
      <div class="goto-link">
        <Button variant="link" @click="()=>{
          router.push({name:'LoginForm'})
        }"> Go to Login </Button>
      </div>
    </div>
    <Button type="submit" severity="secondary">
      <FontAwesomeIcon :icon="faChampagneGlasses" />
      Register
    </Button>
  </Form>
</template>

<script setup lang="ts">
import { Form, FormSubmitEvent } from "@primevue/forms";
import { Button, IftaLabel, InputText, Message } from "primevue";
import { reactive } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faChampagneGlasses } from "@fortawesome/free-solid-svg-icons";
import { signup } from "@/request/authorization";
import { router } from "@/router";
import { message } from 'ant-design-vue'
import { useUserStore } from "@/stores/userStore";

const userStore = useUserStore()
const initialValues = reactive({
  username: "",
  password: "",
  repeatPassword: "",
  email: "",
});

const resolver = ({ values }: any) => {
  const errors: any = {};
  const passwordRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$/;

  if (!values.username) {
    errors.username = [{ message: "Username is required." }];
  }
  if (!values.password) {
    errors.password = [{ message: "Password is required." }];
  } else if (!passwordRegex.test(values.password)) {
    errors.repeatPassword = [
      {
        message:
          "Password must include uppercase, lowercase, number and special character.",
      },
    ];
  } else if (values.password.length < 8) {
    errors.password = [
      { message: "Password must be at least 8 characters long." },
    ];
  }
  if (values.repeatPassword !== values.password) {
    errors.repeatPassword = [{ message: "Your password is not same." }];
  }
  if (!values.email) {
    errors.email = [{ message: "Email is required." }];
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email)) {
    errors.email = [{ message: "Invalid email format." }];
  }

  return {
    values, // (Optional) Used to pass current form values to submit event.
    errors,
  };
};

const onFormSubmit = async (e: FormSubmitEvent) => {
  if (e.valid) {
    const res = await signup({
      username: e.values.username,
      password: e.values.password,
      email: e.values.email,
    });
    
    if (typeof res !== "number") {
      userStore.login(e.values.username)
      await router.push({ name: "LoginForm" });
      message.success("Register successful, you can login now.")
    } else {
      message.error("Register failed, Username or password is incorrect.")
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
    color: var(--primary-text-color);
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
    color: var(--primary-background-color);
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

