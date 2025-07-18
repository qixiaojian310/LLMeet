<template>
  <div class="toolbar-view">
    <div class="toolbar-view_header">
      <ToolbarButton
        v-for="button in props.buttons"
        :key="button.title"
        :title="button.title"
        :icon="button.icon"
        :handle-click="
          () => {
            redirect(button.path);
          }
        "
      >
        <FontAwesomeIcon :icon="button.icon" />
        <p>{{ button.title }}</p>
      </ToolbarButton>
    </div>
    <div class="toolbar-view_bottom">
      <ToolbarButton title="User" :icon="faUser" :isMini="true" />
      <ToolbarButton title="Setting" :icon="faGear" :isMini="true" />
      <ToolbarButton
        title="Logout"
        :icon="faRightFromBracket"
        :handleClick="logout"
        :isMini="true"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { faUser, faGear, faRightFromBracket } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { ToolbarItem } from '@/types/mainLayout/toolbar';
import { router } from '@/router';
import { useUserStore } from '@/stores/userStore';
import { userStaticStore } from '@/utils/staticStore';
import { message } from 'ant-design-vue';
import ToolbarButton from './ToolbarButton.vue';

const props = defineProps({
  buttons: {
    type: Array<ToolbarItem>,
    default: () => []
  }
});
const logout = async () => {
  const userStore = useUserStore();
  await userStaticStore.delete('accessToken');
  await userStaticStore.save();
  userStore.logout();
  router.push({ name: 'RegisterForm' });
  message.success('Logout successful.');
};
const redirect = (path: string) => {
  router.push({ path: `/home/${path}` });
};
</script>

<style scoped lang="scss">
.toolbar-view {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  padding: 1rem 0;
  &_header {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 100%;
  }
  &_bottom {
    display: flex;
    flex-direction: column;
    justify-content: end;
    width: 100%;
    padding: 0 1rem;
    flex: 1;
  }
}
</style>
