<template>
    <div>
      <Navbar class="padding pt-2" />
      <div class="padding py-4">
        <slot />
      </div>
      <Footer class="padding" />
    </div>
</template>

<script lang="ts" setup>

</script>

<style scoped>
.padding {
@apply px-4 sm:px-6 md:px-14 lg:px-36;
}
</style>