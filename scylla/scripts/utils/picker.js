(function () {
  const STORAGE_KEY = 'userAvatarSrc';
  const DEFAULT_AVATAR = '../assets/avatar_boy.png';
  const PRESET_AVATARS = [
    { src: '../assets/3d-illustration-with-online-avatar.png', label: 'Girl' },
    { src: '../assets/avatar_boy.png',  label: 'Boy'  },
    { src: '../assets/avatar_girl2.png', label: 'Girl' },
    { src: '../assets/avatar_boy2.png',  label: 'Boy'  },
    { src: '../assets/avatar_girl3.png', label: 'Girl' },
    { src: '../assets/avatar_boy3.png',  label: 'Boy'  },
  ];

  const container = document.getElementById('userAvatarContainer');
  if (!container) return;

  const savedSrc = localStorage.getItem(STORAGE_KEY);
  const avatarSrc = savedSrc || DEFAULT_AVATAR;

  container.innerHTML = `
    <img id="userAvatar"
         src="${avatarSrc}"
         alt="Avatar do usuário"
         width="40" height="40"
         style="border-radius:50%;object-fit:cover;width:100%;height:100%;cursor:pointer;" />
  `;

  const avatarImg = document.getElementById('userAvatar');
  const picker   = document.getElementById('avatarPicker');
  const grid     = document.getElementById('avatarGrid');
  const closeBtn = document.getElementById('closeAvatarPicker');
  const clearBtn = document.getElementById('clearAvatar');
  const uploadBtn= document.getElementById('uploadAvatar');
  const fileInput= document.getElementById('avatarFile');

  if (!picker || !grid || !closeBtn || !clearBtn || !uploadBtn || !fileInput) return;

  function openPicker() {
    renderOptions(localStorage.getItem(STORAGE_KEY) || avatarImg.src);
    picker.hidden = false;
    picker.setAttribute('aria-hidden','false');
    grid.querySelector('.ap-avatar-item')?.focus();
    document.addEventListener('keydown', escToClose);
    picker.addEventListener('click', backdropClose);
  }
  function closePicker() {
    picker.hidden = true;
    picker.setAttribute('aria-hidden','true');
    document.removeEventListener('keydown', escToClose);
    picker.removeEventListener('click', backdropClose);
    avatarImg.focus?.();
  }
  function escToClose(e){ if (e.key === 'Escape') closePicker(); }
  function backdropClose(e){ if (e.target === picker) closePicker(); }

  function renderOptions(selectedSrc) {
    grid.innerHTML = '';
    PRESET_AVATARS.forEach(opt => {
      const btn = document.createElement('button');
      btn.className = 'ap-avatar-item' + (opt.src === selectedSrc ? ' selected' : '');
      btn.type = 'button';
      btn.title = opt.label;
      btn.setAttribute('role','listitem');

      const img = document.createElement('img');
      img.src = opt.src;
      img.alt = opt.label;
      btn.appendChild(img);

      btn.addEventListener('click', () => {
        setAvatar(opt.src);
        grid.querySelectorAll('.ap-avatar-item').forEach(el => el.classList.remove('selected'));
        btn.classList.add('selected');
        closePicker();
      });

      grid.appendChild(btn);
    });
  }

  function setAvatar(src) {
    avatarImg.src = src;
    localStorage.setItem(STORAGE_KEY, src);
  }
  function clearAvatar() {
    localStorage.removeItem(STORAGE_KEY);
    avatarImg.src = DEFAULT_AVATAR;
  }

  uploadBtn.addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', e => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      try {
        setAvatar(reader.result);
        closePicker();
      } catch (err) { console.error(err); }
    };
    reader.readAsDataURL(file);
  });

  avatarImg.addEventListener('click', openPicker);
  closeBtn.addEventListener('click', closePicker);
  clearBtn.addEventListener('click', clearAvatar);

  avatarImg.addEventListener('error', () => {
    if (avatarImg.src.includes(DEFAULT_AVATAR)) return;
    clearAvatar();
  });
})();