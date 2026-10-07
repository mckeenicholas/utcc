<script lang="ts">
import type { User } from "#lib/types.js";

interface Props {
	user: User;
}

const { user }: Props = $props();
</script>

<a href="/persons/{user.id}" class="group block">
	<div
		class="flex w-full cursor-pointer items-center justify-between border border-border bg-surface p-3 transition-colors hover:border-brand"
	>
		<div class="flex min-w-0 items-center gap-3">
			<div
				class="flex h-8 w-8 shrink-0 items-center justify-center rounded-sm bg-surface-muted text-xs font-bold text-brand transition-colors group-hover:bg-uoft-blue group-hover:text-white"
			>
				{user.name.charAt(0).toUpperCase()}
			</div>
			<div class="truncate">
				<p class="truncate text-sm font-medium text-main transition-colors group-hover:text-brand">
					{user.name}
				</p>
				{#if user.student_designator}
					<span class="rounded-sm bg-surface-muted px-1.5 py-0.5 text-[10px] font-medium text-secondary uppercase">
						{user.student_designator}
					</span>
				{/if}
			</div>
		</div>

		<span class="text-xs text-muted transition-colors group-hover:text-brand">&rarr;</span>
	</div>
</a>
