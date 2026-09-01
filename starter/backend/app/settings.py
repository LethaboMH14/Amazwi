from enum import Enum
from pathlib import Path
from typing import Literal
from pydantic import BaseModel, SecretStr, model_validator
class RuntimeMode(str,Enum): TEST="test"; DEMO="demo"; PRODUCTION="production"
class Settings(BaseModel):
 mode:RuntimeMode; database_url:str; private_audio_root:Path; audio_signing_key:SecretStr; auth_backend:Literal["demo_header","external"]; rate_limit_backend:Literal["in_memory","external"]; demo_controls_enabled:bool=False; demo_control_token:SecretStr|None=None; failure_injection_enabled:bool=False
 @model_validator(mode="after")
 def validate_boundaries(self):
  errors=[]
  if self.mode is RuntimeMode.PRODUCTION:
   if self.auth_backend!="external":errors.append("production requires external authentication")
   if self.rate_limit_backend!="external":errors.append("production requires an external distributed rate limiter")
   if self.demo_controls_enabled or self.demo_control_token is not None or self.failure_injection_enabled:errors.append("demo controls are forbidden in production")
  if errors:raise ValueError("; ".join(errors))
  return self
 @classmethod
 def test_defaults(cls,**overrides):
  values=dict(mode=RuntimeMode.TEST,database_url="postgresql://localhost/amazwi_test",private_audio_root=Path(".pytest-audio"),audio_signing_key="test-audio-key",auth_backend="demo_header",rate_limit_backend="in_memory",demo_controls_enabled=True,demo_control_token="test-demo-token")
  values.update(overrides);return cls(**values)
