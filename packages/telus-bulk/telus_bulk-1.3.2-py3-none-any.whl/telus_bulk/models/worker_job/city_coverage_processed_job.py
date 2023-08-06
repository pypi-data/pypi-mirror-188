from typing import List, Optional
from fastapi_camelcase import CamelModel
from telus_bulk.models.worker_job.address_processing_job import AddressProcessingJob


class RelatedParty(CamelModel):
    partner_name: str
    contact_method: str
    contact_email: Optional[str] = None
    province_full_coverage: Optional[bool] = True
    city_coverage: Optional[bool] = False
    status: Optional[str] = None


class CityCoverageProcessedJob(AddressProcessingJob):
    related_party: List[RelatedParty] = []
