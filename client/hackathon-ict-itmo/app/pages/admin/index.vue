<template>
  <div>
    <Card>
      <div class="header-row">
        <h1>Администрирование</h1>
        <Button variant="secondary" @click="load" :disabled="loading">
          Обновить
        </Button>
      </div>

      <div v-if="loading" class="hint">Загрузка...</div>

      <table v-else class="users-table">
        <thead>
          <tr>
            <th>Пользователь</th>
            <th>Email</th>
            <th>Роли</th>
            <th></th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="u in users" :key="u.id">
            <td>{{ u.firstName }} {{ u.lastName }}</td>
            <td>{{ u.email }}</td>

            <td>
              <div class="roles-row">
                <span
                  v-for="role in roles"
                  :key="role"
                  class="role-badge"
                  :class="{ active: u.roles.includes(role) }"
                >
                  {{ role }}
                </span>
              </div>

              <div class="role-actions">
                <Button
                  v-for="role in roles"
                  :key="role"
                  variant="secondary"
                  :disabled="busyUserId === u.id || loading"
                  @click="assign(u.id, role)"
                >
                  Назначить {{ role }}
                </Button>
              </div>
            </td>

            <td class="user-actions">
              <Button
                variant="primary"
                :disabled="deleteUserId === u.id || loading"
                @click="remove(u.id)"
              >
                Удалить
              </Button>
            </td>
          </tr>
        </tbody>
      </table>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue"
import Card from "~/components/ui/Card.vue"
import Button from "~/components/ui/Button.vue"
import { useAdminStore } from "~/stores/adminStore"
import type { UserRole } from "../../../types/user"

definePageMeta({
  layout: "org"
})

const roles: UserRole[] = ["participant", "organizer", "admin"]

const store = useAdminStore()

const users = computed(() => store.getUsers)
const loading = computed(() => store.loading)

const busyUserId = ref<string | null>(null)
const deleteUserId = ref<string | null>(null)

async function load() {
  await store.fetchAllUsers(1)
}

async function assign(userId: string, role: UserRole) {
  if (busyUserId.value) return
  busyUserId.value = userId
  try {
    await store.assignRole(userId, role)
    await store.fetchAllUsers(1)
  } catch (e) {
    console.error(e)
    alert("Не удалось назначить роль")
  } finally {
    busyUserId.value = null
  }
}

async function remove(userId: string) {
  const ok = window.confirm("Удалить пользователя?")
  if (!ok) return
  if (deleteUserId.value) return
  deleteUserId.value = userId
  try {
    await store.deleteUser(userId)
    await store.fetchAllUsers(1)
  } catch (e) {
    console.error(e)
    alert("Не удалось удалить пользователя")
  } finally {
    deleteUserId.value = null
  }
}

onMounted(() => {
  load().catch((e) => {
    console.error(e)
    alert("Не удалось загрузить пользователей")
  })
})
</script>

<style scoped>
.header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.hint {
  margin-top: 0.75rem;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.users-table th,
.users-table td {
  border-bottom: 1px solid #eaeaea;
  padding: 0.75rem 0.5rem;
  vertical-align: top;
}

.roles-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.role-badge {
  padding: 0.25rem 0.5rem;
  border: 1px solid #d0d0d0;
  border-radius: 0.5rem;
  font-size: 0.85rem;
  color: #555;
  background: #fff;
}

.role-badge.active {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.role-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.user-actions {
  white-space: nowrap;
}
</style>

