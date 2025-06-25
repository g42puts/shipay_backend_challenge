from datetime import datetime

from sqlalchemy.orm import Session

from app.factories.infra.auth.make_password_helper import make_password_helper
from app.infra.db.db import engine
from app.models import Role, User, Claim, UserClaim
from app.configs.configs import configs
from app.utils.utils import claims


def seed():
    with Session(bind=engine) as session:
        try:
            # Roles
            admin_role = session.query(Role).filter_by(description="admin").first()
            user_role = session.query(Role).filter_by(description="user").first()
            if not admin_role:
                admin_role = Role(description="admin")
                session.add(admin_role)
            if not user_role:
                user_role = Role(description="user")
                session.add(user_role)

            # Claims
            claims_to_seed = claims.values()
            existing_claims = {
                claim.description for claim in session.query(Claim).all()
            }
            for desc in claims_to_seed:
                if desc not in existing_claims:
                    session.add(Claim(description=desc))
            session.commit()

            # Usuário admin
            admin_email = configs.DEFAULT_ADMIN_EMAIL or "admin@admin.com"
            admin_password = configs.DEFAULT_ADMIN_PASSWORD or "admin123"
            admin_user = session.query(User).filter_by(email=admin_email).first()
            if not admin_user:
                admin_user = User(
                    name="Administrador",
                    email=admin_email,
                    password=make_password_helper().hash(admin_password),
                    role_id=admin_role.id,
                    created_at=datetime.now(),
                )
                session.add(admin_user)
                session.commit()
                session.refresh(admin_user)

                print(f"Usuário admin criado: {admin_email} / {admin_password}")
            else:
                print(f"Usuário admin já existe: {admin_email}")

            # Associar todos os claims ao admin, sem duplicidade
            all_claims = session.query(Claim).all()
            admin_claim_ids = {
                uc.claim_id
                for uc in session.query(UserClaim).filter_by(user_id=admin_user.id)
            }
            new_user_claims = [
                UserClaim(user_id=admin_user.id, claim_id=claim.id)
                for claim in all_claims
                if claim.id not in admin_claim_ids
            ]
            if new_user_claims:
                session.bulk_save_objects(new_user_claims)
                session.commit()
        finally:
            session.close()


if __name__ == "__main__":
    seed()  # pragma: no cover
